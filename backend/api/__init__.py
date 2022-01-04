# Import the required libraries
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db_path = os.path.join(os.path.dirname(__file__), 'database/data.sqlite')
"""Application-factory pattern"""
app = Flask(__name__)
app.config["SECRET_KEY"] = 'ryuzvki_flask_key'  # keep this key secret during production
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False

# Create various application instances
# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow()
cors = CORS(app)
bcrypt = Bcrypt(app)
ma.init_app(app)
cors.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

"""Routes-factory pattern"""
from api.circonscription import routes
from api.election import routes
from api.elector import routes
from api.party import routes
from api.candidate import routes
from api.vizualizer import map
from api.check_registration import verification
from api.bureau_change_request import changement
