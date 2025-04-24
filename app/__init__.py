from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from app.models import User
from flask_login import LoginManager
from app.extensions import db, login_manager, migrate
from .routes.expense_routes import expenses_bp
from app.routes.expense_routes import expenses_bp



login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth_routes import auth_bp
    # from .routes.expense_routes import expense_bp
    # from .routes.prediction_routes import prediction_bp
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.routes.auth_routes import auth_bp
    from app.routes.expense_routes import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    # app.register_blueprint(prediction_bp)
    login_manager.login_view = 'auth.login'

    return app  





    return app
