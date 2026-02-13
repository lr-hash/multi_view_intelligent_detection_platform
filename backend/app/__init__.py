from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app import models
    from app import commands
    commands.register_commands(app)
    
    # Register SocketIO events
    with app.app_context():
        from app import socket_events

    return app
