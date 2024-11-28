from flask import Flask, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

# Set a secret key for the session
secret_key = os.getenv('APP_SECRET_KEY')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  


# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

if google is None:
    raise ValueError("Failed to register Google OAuth client")

@app.route('/')
@login_required
def index():
    email = dict(session).get('email', None)
    return f'Hello, {email}!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    if token is None:
        return 'Authorization failed.', 400

    resp = google.get('userinfo')
    user_info = resp.json()
    if user_info is None:
        return 'Failed to fetch user info.', 400

    # Store user info in session
    session['email'] = user_info['email']
    session.permanent = True  # make the session permanent so it keeps existing after browser gets closed

    # Query or create user in the database
    email = user_info['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)

    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


