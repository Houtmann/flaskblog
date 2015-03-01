
from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField, HiddenField,
                     SubmitField)
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo,
                                regexp, ValidationError)
from flask_babelex import lazy_gettext as _

from models import Utilisateur

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=_("You can only use letters, numbers or dashes."))


class LoginForm(Form):
    login = StringField('Username')
    password = PasswordField('Password')

    submit = SubmitField(_("Login"))
