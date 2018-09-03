from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '123123123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
