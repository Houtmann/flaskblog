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



profil = Blueprint('profil', __name__)



@profil.route('/home', methods=["GET", "POST"])
@login_required
def home():
    return render_template('profil.html')




    
   
    
