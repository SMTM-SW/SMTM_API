import os

HOST_API = os.environ['HOST_API']
HOST_CLIENT = os.environ['HOST_CLIENT']
HOST_CRAWLER = os.environ['HOST_CRAWLER']

# flask
SECRET_KEY = os.environ['SECRET_KEY']

# yagmail
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

# db
DATABASE_HOST = 'localhost:3306'
DATABASE_USERNAME = 'smtm'
DATABASE_PASSWORD = 'kbv@p!23ay'
DEFAULT_DATABASE = 'smtm_application'
OAUTH_DATABASE = 'smtm_oauth'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DATABASE_USERNAME,
                                                                   DATABASE_PASSWORD,
                                                                   DATABASE_HOST,
                                                                   DEFAULT_DATABASE)
SQLALCHEMY_BINDS = {
    'smtm_application': "mysql+pymysql://{0}:{1}@{2}/{3}".format(DATABASE_USERNAME,
                                                                 DATABASE_PASSWORD,
                                                                 DATABASE_HOST,
                                                                 DEFAULT_DATABASE),
    'smtm_oauth': "mysql+pymysql://{0}:{1}@{2}/{3}".format(DATABASE_USERNAME,
                                                           DATABASE_PASSWORD,
                                                           DATABASE_HOST,
                                                           OAUTH_DATABASE)
}

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = 'True'

TEMPLATES_AUTO_RELOAD = True
