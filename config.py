from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class App:

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123qwe@localhost/dashboard'
    db = SQLAlchemy(app)

    