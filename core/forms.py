
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

    

class RegisterForm(Form):
    username = StringField(_("Username"), validators=[
        DataRequired(message=_("A Username is required.")),
        is_username])

    email = StringField(_("E-Mail Address"), validators=[
        DataRequired(message=_("A E-Mail Address is required.")),
        Email(message=_("Invalid E-Mail Address."))])

    name = StringField(_('name'))
    firstname = StringField(_('firstname'))

    password = PasswordField(_('Password'), validators=[
        InputRequired(),
        EqualTo('confirm_password', message=_('Passwords must match.'))])

    confirm_password = PasswordField(_('Confirm Password'))

   
    submit = SubmitField(_("Register"))

    def validate_username(self, field):
        user = Utilisateur.select().where(Utilisateur.pseudo==field.data).first()
        if user:
            raise ValidationError(_("This Username is already taken."))

    def validate_email(self, field):
        email = Utilisateur.select().where(Utilisateur.email==field.data).first()
        if email:
            raise ValidationError(_("This E-Mail Address is already taken."))

    def save(self):
    
        Utilisateur.create(nom = self.name.data,
                           prenom = self.firstname.data,
                           pseudo = self.username.data,
                           email = self.email.data,
                           password = Utilisateur.hash_password(self.password.data))
        
            
    

