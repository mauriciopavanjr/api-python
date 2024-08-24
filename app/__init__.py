from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

if os.getenv('ENVIRONMENT') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('ENVIRONMENT') == 'development':
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models