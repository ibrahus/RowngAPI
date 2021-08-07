import os
import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import datetime
import json

database_path = os.getenv(
    'DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/fsnd-rowng-api')
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def setup_migrations(app):
    migrate = Migrate(app, db)


def create_and_drop_all():
    db.drop_all()
    db.create_all()

    # create a new vendor
    vendor = Vendor(
        name='Vendor 1 name',
        city='Riyadh',
        address='Vendor 1 address',
        start_duty_time=datetime.time(9),
        end_duty_time=datetime.time(9),
    )
    vendor.insert()

    # create new user
    user = User(
        name='User 1 name',
        city='Riyadh',
    )
    user.insert()

    # create new booking
    booking = Booking(
        booking_date=datetime.datetime.now(),
        vendor_id=1,
        user_id=1,
        services=[1, 2],
    )
    booking.insert()

    # create new services
    service = Service(
        service_duration=datetime.time(1),
        service_name='Service 1 name',
        service_price=100,
        vendor_id=1,
    )
    service.insert()


class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    start_duty_time = db.Column(db.Time)
    end_duty_time = db.Column(db.Time)
    services = db.relationship('Service', backref='vendor', lazy=True)
    bookings = db.relationship('Booking', backref='vendor', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'address': self.address,
            'start_duty_time': str(self.start_duty_time),
            'end_duty_time': str(self.end_duty_time),
        }


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
        }


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String)
    service_price = db.Column(db.Integer)
    service_duration = db.Column(db.Time)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'service_price': self.service_price,
            'service_duration': str(self.service_duration)
        }


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    services = db.Column(db.ARRAY(db.Integer))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'booking_date': self.booking_date,
            'vendor_id': self.vendor_id,
            'user_id': self.user_id,
            'services': self.services,
        }
