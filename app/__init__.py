from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
#import pymysql.cursors

#database (string: "PAD.db")#
"""
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='passwd',
                             database='pad.db',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('email@gmail.com', 'senha1234'))
    
    connection.commit()

    with connection.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('email@gmail.com',))
        result = cursor.fetchone()
"""

login_manager = LoginManager()
login_manager.login_view = 'bp.login'
login_manager.session_protection = "strong"
bcrypt = Bcrypt()
db = SQLAlchemy()


def app_config() -> Flask:
    app = Flask(__name__, template_folder='web/template', static_folder='web/static')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = '6454374a821103b2925319e2a2e8f9d4'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../pad.db"
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
    
    
    return app
