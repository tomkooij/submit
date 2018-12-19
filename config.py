import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'you-will-never-guess'

    DEBUG = True
    FLASK_DEBUG = True

    # local dhfdgr3xy757eufhfgfAGDSHRjhtr5456653wdvbmWESGnhgtutfhgfd43424tes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # pythonanywhere
    MYSQLSERVER = 'tomkooij.mysql.pythonanywhere-services.com'
    MYSQLDB = 'tomkooij$aanmeldr'
    MYSQLUSER = 'tomkooij'
    MYSQLPASS = 'fake'
    #SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    #username=MYSQLUSER,
    #password=MYSQLPASS,
    #hostname=MYSQLSERVER,
    #databasename=MYSQLDB,
    #)

    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_DEFAULT_DEST = 'uploads'
    UPLOADED_DEFAULT_ALLOW = ('py', 'ipynb')
    UPLOAD_FOLDER = os.path.join(basedir, UPLOADED_DEFAULT_DEST)
