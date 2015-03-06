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
from core.main import *

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
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return inner

def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('main.test'))
        return f(*args, **kwargs)
    return inner
