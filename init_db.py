from app import db, app
from flask_migrate import Migrate

with app.app_context():
    migrate = Migrate(app, db)
    db.create_all()