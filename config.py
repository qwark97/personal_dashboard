from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

class App:

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123qwe@localhost/dashboard'
    app.config['SECRET_KEY'] = 'dtAXrOu2cVjeLCORr8p1'
    db = SQLAlchemy(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
