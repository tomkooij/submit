import re

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES

from jinja2 import evalcontextfilter, Markup, escape


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

pycode = UploadSet('default') #, extensions=('py', 'ipynb'))
configure_uploads(app, pycode)
patch_request_class(app, 64 * 1024) # max upload size 64Kb


# nl2br jinja filter
# http://flask.pocoo.org/snippets/28/
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


from app import routes, models, admin


@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))
