from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "web.login"
login_manager.login_message = "请先登录后再操作。"


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

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
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    if app.config.get("AUTO_CREATE_DB"):
        # 个人站点默认自动建表，避免首次部署或本地运行时因为空库直接 500。
        with app.app_context():
            db.create_all()

    return app
