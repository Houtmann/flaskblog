from functools import wraps

from flask import abort
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack, session
from flask import g
from models import bdd

t = bdd()

user = t.check_level('hhoutmann@gmail.com')
print(user['level'])
