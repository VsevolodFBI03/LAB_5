from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '417-290-505'
app.config.from_object('config')
db = SQLAlchemy(app)

from app.models import Region, CarTaxParam