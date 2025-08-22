from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
from importer import import_csv

from database import db
from models import Beer, User
from datetime import datetime

from blueprints.beer import beer_bp # Import beer blueprint
from blueprints.auth import auth_bp # Import auth blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'a_very_secret_key'
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login' # Set the login view to blueprint's login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(beer_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
