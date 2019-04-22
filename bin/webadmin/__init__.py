import os
import logging
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
from ConfigReader import configuration

loggingLevel = logging.DEBUG

# Initiate the logging functions with the correct level
if loggingLevel == logging.DEBUG:
	logging.basicConfig(format='%(levelname)s %(funcName)s - %(message)s', level=loggingLevel)
else:
	logging.basicConfig(format='%(levelname)s - %(message)s', level=loggingLevel)
# logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# logging.getLogger().setLevel(logging.DEBUG)

try:
   DBImport_Home = os.environ['DBIMPORT_HOME']
except KeyError:
   logging.error("System Environment Variable DBIMPORT_HOME is not set")
   sys.exit(1)

# Fetch configuration about MySQL database and how to connect to it
mysql_hostname = configuration.get("Database", "mysql_hostname")
mysql_port =     configuration.get("Database", "mysql_port")
mysql_database = configuration.get("Database", "mysql_database")
mysql_username = configuration.get("Database", "mysql_username")
mysql_password = configuration.get("Database", "mysql_password")

app = Flask(__name__)
# app.config.from_object('config')

app.config.update(
# import os
# from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
# basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h',

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DBImport_Home + '/conf/webadmin.db',
#SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
#SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

SQLALCHEMY_BINDS = {
	'DBImport': 'mysql://' + mysql_username + ':' + mysql_password + '@' + mysql_hostname + ':' + mysql_port + '/' + mysql_database,
	'memory': 'sqlite://'
},

# Flask-WTF flag for CSRF
CSRF_ENABLED = True,

#------------------------------
# GLOBALS FOR APP Builder 
#------------------------------
# Uncomment to setup Your App name
APP_NAME = "DBImport",

# Uncomment to setup Setup an App icon
#APP_ICON = "static/img/logo.jpg"

#----------------------------------------------------
# AUTHENTICATION CONFIG
#----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
AUTH_TYPE = AUTH_DB,

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = 'Admin',

# Uncomment to setup Public role name, no authentication needed
AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = False,

# The default user self registration role
#AUTH_USER_REGISTRATION_ROLE = "Public"

# When using LDAP Auth, setup the ldap server
#AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
#OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
#---------------------------------------------------
# Babel config for translations
#---------------------------------------------------
# Setup default language
#BABEL_DEFAULT_LOCALE = 'en'
# Your application default translation path
#BABEL_DEFAULT_FOLDER = 'translations'
# The allowed translation for you app
#LANGUAGES = {
#    'en': {'flag':'gb', 'name':'English'},
#    'pt': {'flag':'pt', 'name':'Portuguese'},
#    'pt_BR': {'flag':'br', 'name': 'Pt Brazil'},
#    'es': {'flag':'es', 'name':'Spanish'},
#    'de': {'flag':'de', 'name':'German'},
#    'zh': {'flag':'cn', 'name':'Chinese'},
#    'ru': {'flag':'ru', 'name':'Russian'},
#    'pl': {'flag':'pl', 'name':'Polish'}
#}
#---------------------------------------------------
# Image and file configuration
#---------------------------------------------------
# The file upload folder, when using models with files
#UPLOAD_FOLDER = basedir + '/app/static/uploads/',

# The image upload folder, when using models with images
#IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/',

# The image upload url, when using models with images
#IMG_UPLOAD_URL = '/static/uploads/',
# Setup image size default is (300, 200, True)
#IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
#APP_THEME = "cerulean.css"
#APP_THEME = "amelia.css"
#APP_THEME = "cosmo.css"
#APP_THEME = "cyborg.css"  
#APP_THEME = "flatly.css"
#APP_THEME = "journal.css"
APP_THEME = "readable.css"
#APP_THEME = "simplex.css"
#APP_THEME = "slate.css"   
#APP_THEME = "spacelab.css"
#APP_THEME = "united.css"
#APP_THEME = "yeti.css"

# FAB_API_SWAGGER_UI = True
)

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

from webadmin import views
