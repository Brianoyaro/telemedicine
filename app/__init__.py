from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
# from flask_mail import Mail
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
#migrate = Migrate()
login = LoginManager()
#mail = Mail()
login.login_view = 'auth.login'

def create_app(config=Config):
    """creates an instance of an application"""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login.init_app(app)
    #mail.init_app(app)
    #migrate.init_app(app, db)

    from app import models
    from app.hospital import bp as hospital_bp
    from app.patient import bp as patient_bp

    app.register_blueprint(hospital_bp)
    app.register_blueprint(patient_bp)
    return app