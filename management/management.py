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
from decorator import admin_required, login_required, is_admin


management = Blueprint('management', __name__)


@management.route('/delete_comment/<int:comment_id>', methods=["GET", "POST"])
@admin_required
def delete_comment(comment_id):
    Commentaires.delete_comment(comment_id)
    return redirect(url_for('main.index'))

@management.route('/management', methods=["GET", "POST"])
@admin_required
def admin():
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


@management.route('/management_utils', methods=["GET", "POST"])
@admin_required
def admin_utils():
    utilisateur = Utilisateur.select(Utilisateur.email,
                                      Utilisateur.pseudo,
                                      Utilisateur.date_register,
                                      Utilisateur.reputation)
    return render_template('management_utilisateurs.html', loader = utilisateur)





   
    
