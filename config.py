import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'you-will-never-guess-hoop-ik-dan'

    DEBUG = True
    FLASK_DEBUG = True

    MYSQLSERVER = 'htpc.fritz.box' #'127.0.0.1'
    MYSQLSERVERPORT = 32000 #3206
    MYSQLDB = 'submit'
    MYSQLUSER = 'root'
    MYSQLPASS = 'rootfoobar'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}:{port}/{databasename}".format(
        username=MYSQLUSER,
        password=MYSQLPASS,
        hostname=MYSQLSERVER,
        databasename=MYSQLDB,
        port=MYSQLSERVERPORT,
    )

    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_DEFAULT_DEST = 'uploads'
    UPLOADED_DEFAULT_ALLOW = ('py', 'ipynb')
    UPLOAD_FOLDER = os.path.join(basedir, UPLOADED_DEFAULT_DEST)
