from flask import Flask


# configuration
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_URI = 'sqlite:///' + DATABASE
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE


import alayatodo.views
import alayatodo.models
