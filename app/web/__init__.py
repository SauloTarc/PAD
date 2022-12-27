from flask import Flask
from app.web.routes import bp


def register_routes(app: Flask):
    app.register_blueprint(bp)