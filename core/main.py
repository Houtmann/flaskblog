# -*- coding: utf-8 -*-
from functools import wraps
import os
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack, session, abort, Blueprint
from flask import g
import jinja2
from jinja2 import Template
import sys
from models import Utilisateur, Messages, Commentaires
import bcrypt
from peewee import *
from playhouse.flask_utils import PaginatedQuery
from flask_peewee.utils import *
import bbcode
from flaskext.markdown import Markdown
from decorator import admin_required, login_required, is_admin
from .forms import LoginForm, RegisterForm


main = Blueprint('main', __name__)

def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['email'] = user.email



@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Utilisateur.get(Utilisateur.email == form.login.data)
        except Utilisateur.DoesNotExist:
            flash('''Nom d'utilisateur incorrect !''')
            return redirect(url_for('main.login'))
            
        if bcrypt.hashpw(form.password.data.encode('latin1'),
                         user.password.encode('latin1')) == user.password.encode('latin1'):
                auth_user(user)
                return redirect(url_for('main.index'))
        else:
            abort(404) 
    return render_template('login.html', form=form)



@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): 
        user = form.save()   
        return redirect(url_for('main.login'))
    
    return render_template("register.html", form=form)


@main.route("/", methods=["GET", "POST"])
@main.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    message = Messages.select(Messages.id,
                              Messages.titre,
                              Messages.content,
                              Messages.tags,
                              Messages.date_post,
                              Messages.user).join(Utilisateur, JOIN_LEFT_OUTER).order_by(Messages.date_post.desc())

    if request.method == 'POST':
        article(request.form['id'])
    return object_list('index.html', message, paginate_by=4)
    

@main.route("/add_article", methods=["GET", "POST"])
@login_required
def add_article():
    if request.method == 'POST':
        try:
            user = Utilisateur.get(Utilisateur.email == session.get('email'))
            Messages.add_message(request.form['titre'],
                                 request.form['message'],
                                 user.id,
                                 request.form['tags'])

            return redirect(url_for('main.index'))
        except Exception:
            flash('''Le contenu vide n'est pas autorisé''')
    return render_template('add_article.html')


@main.route('/delete_article/<int:message_id>', methods=["GET", "POST"])
@admin_required
def delete_article(message_id):
    Messages.delete_message(message_id)
    return redirect(url_for('main.index'))


@main.route('/<value>', methods=["GET", "POST"])
@login_required
def article(value):
    message = Messages.select(Messages.id,
                              Messages.titre,
                              Messages.content,
                              Messages.date_post,
                              Messages.user).join(Utilisateur, JOIN_LEFT_OUTER).where(Messages.id == value)

    coms = Commentaires.select(Commentaires.id,
                               Commentaires.content,
                               Commentaires.date,
                               Messages.user,
                               Utilisateur.pseudo).join(Messages, JOIN_LEFT_OUTER).join(Utilisateur,
                                                                                        JOIN_LEFT_OUTER).where(
        Messages.id == value)

    user_id = session.get('user_id')  # Pour associer la session à l'user id
    if request.method == 'POST':
        Commentaires.add_commentaire(request.form['commentaire'], value, user_id)
        return redirect(value)

    return render_template('article.html',
                           loader=message, com_loader=coms)










    
   
    
