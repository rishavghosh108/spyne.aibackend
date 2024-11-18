from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spyne.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db=SQLAlchemy(app)
migrate=Migrate(app,db)