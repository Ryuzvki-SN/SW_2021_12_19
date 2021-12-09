# Import the required libraries
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db_path = os.path.join(os.path.dirname(__file__), 'database/data.sqlite')
"""Application-factory pattern"""
app = Flask(__name__)
app.config["SECRET_KEY"] = 'ryuzvki learn flask key'  # keep this key secret during production
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False

# Create various application instances
# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow()
cors = CORS(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
ma.init_app(app)
cors.init_app(app)
"""Routes-factory pattern"""
from api.admin import routes
from api.circonscription import routes
from api.electeur import routes
from api.liste import routes
from api.vizualizer import map


