from flask import Flask
from core.main import main
from profil.views import profil
from management.management import management
from models import Utilisateur, Messages, Commentaires
from decorator import is_admin
import bbcode
from jinja2 import Environment, PackageLoader

DEBUG = True
SECRET_KEY = 'hadmagic123456*::5'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('flaskb', silent=True)
environment = Environment()



app.register_blueprint(main)
app.register_blueprint(management)
app.register_blueprint(profil)


app.jinja_env.filters['is_admin'] = is_admin
app.jinja_env.filters['bbcode'] = bbcode.render_html
app.run(host='0.0.0.0', debug=True)
