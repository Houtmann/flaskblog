# -*- coding: utf8 -*-
import os
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack
from flask import g
import jinja2
import sys
import pymysql
import datetime
import bcrypt
from peewee import *



database = MySQLDatabase('dev3', **{'host': '127.0.0.1', 'port': 5001, 'user': 'root', 'password': '123456'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Utilisateur(BaseModel):
    date_register = DateField(default = datetime.date.today())
    email = CharField(unique=True)
    level = TextField(default='user')
    nom = TextField()
    nombre_post = IntegerField(null=True)
    password = TextField()
    prenom = TextField()
    pseudo = TextField()
    reputation = IntegerField(default=0)
      
    def hash_password(password):
        """fonction de hashage du mot de passe en bcrypt"""
        
        passw = password.encode('latin1')
        hashed = bcrypt.hashpw(passw, bcrypt.gensalt())
        return((bcrypt.hashpw(passw, hashed)))
    
    class Meta:
        db_table = 'utilisateur'
        

class Messages(BaseModel):
    content = TextField()
    date_post = DateTimeField()
    titre = TextField()
    user = ForeignKeyField(db_column='Utilisateur_id', rel_model=Utilisateur, to_field='id')

    def add_message(titre, content, user):
        date = datetime.datetime.today()
        if titre and content != '':
            Messages.create(titre=titre,
                        content=content,
                        date_post=date,
                        user=user)
        else:
            raise Exception('Pas de titre et de contenu')

    def delete_message(message_id):
        q = Messages.delete().where(Messages.id == message_id)
        q.execute()
        

    class Meta:
        db_table = 'messages'
        

class Commentaires(BaseModel):
    content = TextField()
    message = ForeignKeyField(db_column='Message_id', rel_model=Messages, to_field='id')
    date = DateTimeField()
    user = IntegerField(db_column='user_id')

    def add_commentaire(content, message, user):
        date = datetime.datetime.today()
        if content != '':
            Commentaires.create(message=message,
                        content=content,
                        date=date,
                        user=user)
        else:
            raise Exception('pas de titre et de contenu')

    class Meta:
        db_table = 'commentaires'


        
def create_tables():
    database.connect()
    database.create_tables([Utilisateur, Messages, Commentaires])







