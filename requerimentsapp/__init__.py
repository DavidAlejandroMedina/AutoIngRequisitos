import os
from flask import Flask


def create_app():
        secret_key_hex = os.urandom(24).hex()
        
        app = Flask(__name__)
        app.secret_key = secret_key_hex
        
        with app.app_context():
                from . import routes
        return app