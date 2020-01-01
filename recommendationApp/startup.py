import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "Main.db"))

    app = Flask(__name__)
    app.secret_key = 'somerandomkey'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_file
    app.config.from_object(__name__)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User,Artist

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
