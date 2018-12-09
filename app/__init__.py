from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

pycode = UploadSet('default') #, extensions=('py', 'ipynb'))
configure_uploads(app, pycode)
patch_request_class(app, 64 * 1024) # max upload size 64Kb

from app import routes, models
