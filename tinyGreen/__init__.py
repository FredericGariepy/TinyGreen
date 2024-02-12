from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
#from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from tinyGreen import myconfigs
# Create a Flask application instance
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = myconfigs.secretdburi

# suggestion: use .env
# secretkey and salt
app.config['SECRET_KEY'] = myconfigs.secretkey
app.config['SECURITY_PASSWORD_SALT'] = myconfigs.secretsalt

# config SMTP mail
app.config['MAIL_SERVER'] = myconfigs.secretemailserver
app.config['MAIL_PORT'] = myconfigs.secretmailport
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = myconfigs.secretemailusr
app.config['MAIL_PASSWORD'] = myconfigs.secretemailpsw
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True

mail = Mail(app)

# Initialize Bcrypt for password hashing
bcrypt =  Bcrypt(app)

# Initialize LoginManager for user authentication
login_manager =  LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Import routes after initializing extensions to avoid circular imports
from tinyGreen import routes