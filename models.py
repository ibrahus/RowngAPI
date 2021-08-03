import os
import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import Column, String, Integer, create_engine
import json
from /app/app.py import app

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()
migrate = Migrate(app, db)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    city = db.Column(String)
    address = db.Column(String)
    # shows = db.relationship('Show', backref='venue', lazy=True)


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'address': self.address
        }