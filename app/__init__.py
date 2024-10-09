from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate  # Dodajemy Flask-Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a strong key

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # Dodajemy obsługę migracji

    # Swagger configuration
    swagger = Swagger(app)

    # Register blueprints
    from .auth import auth_bp
    from .routes import workouts_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(workouts_bp, url_prefix='/')

    return app
