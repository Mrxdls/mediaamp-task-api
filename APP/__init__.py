from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .database import db
from credentials import DATABASE_URL, SECRET_KEY
from .routes.task_routes import task_blueprint
from .routes.user_routes import user_blueprint
from .routes.health_routes import health_blueprint
from APP.Services.rate_limiter import limiter
from flask_migrate import Migrate
from APP.celery_app import celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    celery.conf.update(app.config)
    # Configure database and secrets
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Set SQLAlchemy engine options for connection pooling
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
    }
    
    limiter.init_app(app)
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    # setup migration
    jwt = JWTManager(app)
    # Register blueprints
    app.register_blueprint(task_blueprint, url_prefix='/tasks')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(health_blueprint, url_prefix='/api')
    
    return app