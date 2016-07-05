from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('alayatodo.config.DevelopmentConfig')

db = SQLAlchemy(app)

import alayatodo.views
import alayatodo.models
