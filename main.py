# -*- coding: utf-8 -*-
from functools import wraps
import os
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack, session, abort
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

# configuration
DEBUG = True
SECRET_KEY = 'hadmagic123456*::5'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('flaskb', silent=True)
environment = jinja2.Environment()

POSTS_PER_PAGE = 4


def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['email'] = user.email


def is_admin(current_user):
    current_user = session.get('user_id')
    user = Utilisateur.get(Utilisateur.id == current_user)
    if user.level == 'admin':
        return True
    elif user.level == 'user':
        return False
    else:
        return redirect(url_for('index'))


def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        current_user = session.get('user_id')
        if is_admin(current_user):
            pass
        else:
            return redirect(url_for('index'))
        return f(*args, **kwargs)

    return inner


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return inner


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        try:
            user = Utilisateur.get(Utilisateur.email == request.form['mail'])
        except Utilisateur.DoesNotExist:
            return redirect(url_for('login'))
        if bcrypt.hashpw(request.form['password'].encode('latin1'),
                         user.password.encode('latin1')) == user.password.encode('latin1'):
            auth_user(user)
            return redirect(url_for('index'))
        else:
            abort(404)
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    message = Messages.select(Messages.id,
                              Messages.titre,
                              Messages.content,
                              Messages.date_post,
                              Messages.user).join(Utilisateur, JOIN_LEFT_OUTER).order_by(Messages.date_post.desc())

    if request.method == 'POST':
        article(request.form['id'])
    return object_list('index.html', message, paginate_by=4)


@app.route("/add_article", methods=["GET", "POST"])
@login_required
def add_article():
    if request.method == 'POST':
        try:
            user = Utilisateur.get(Utilisateur.email == session.get('email'))
            Messages.add_message(request.form['titre'],
                                 request.form['message'],
                                 user.id)

            return redirect(url_for('index'))
        except Exception:
            flash('''Le contenu vide n'est pas autorisé''')
    return render_template('add_article.html')


@app.route('/delete_article/<int:message_id>', methods=["GET", "POST"])
@admin_required
def delete_article(message_id):
    Messages.delete_message(message_id)
    return redirect(url_for('index'))

@app.route('/<value>', methods=["GET", "POST"])
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


@app.route('/management', methods=["GET", "POST"])
@admin_required
def management():
    message = Messages.select(Messages.id,
                              Messages.titre,
                              Messages.content,
                              Messages.date_post,
                              Messages.user).join(Utilisateur, JOIN_LEFT_OUTER).order_by(
        Messages.date_post.desc()).limit(5)
    coms = Commentaires.select(Commentaires.id,
                               Commentaires.content,
                               Commentaires.date,
                               Messages.user,
                               Utilisateur.pseudo,
                               Messages.titre,
                               Messages.id).join(Messages, JOIN_LEFT_OUTER).join(Utilisateur, JOIN_LEFT_OUTER).order_by(
        Commentaires.date.desc()).limit(5)
    return render_template('management.html', com_loader=coms,
                           loader=message)


@app.route('/management_utils', methods=["GET", "POST"])
@admin_required
def management_utils():
    return render_template('management_utilisateurs.html')


@app.route('/profil', methods=["GET", "POST"])
@login_required
def profil():
    return render_template('profil.html')


if __name__ == '__main__':
    app.jinja_env.filters['is_admin'] = is_admin
    app.jinja_env.filters['bbcode'] = bbcode.render_html

    app.run(host='0.0.0.0', debug=True)
   
    
