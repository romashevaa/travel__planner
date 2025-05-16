from flask import Flask
from config import Config
from .extensions import db, login_manager
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .views.auth import auth_bp
    from .views.trips import trips_bp
    from .views.blog import blog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(blog_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
