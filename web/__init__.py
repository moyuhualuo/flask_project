from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'index_page'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    db.init_app(app)
    login_manager.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    from .cli import initdb, admin

    app.cli.add_command(initdb)
    app.cli.add_command(admin)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user

    return app
