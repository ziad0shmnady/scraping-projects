# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass
from sqlalchemy import func, desc


class Users(db.Model, UserMixin):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    active = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == "password":
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    user = Users.query.filter_by(username=username, active=1).first()
    return user if user else None


class Aqars(db.Model):

    __tablename__ = "aqar_table"

    # id = db.Column(db.Integer, primary_key=True)
    # ad_id = db.Column(db.String(255), unique=True)
    # ad_license_number = db.Column(db.String(255))
    # title = db.Column(db.String(255))
    # category = db.Column(db.String(255))
    # city = db.Column(db.String(255))
    # district = db.Column(db.String(255))
    # latitude = db.Column(db.String(255))
    # longitude = db.Column(db.String(255))
    # description = db.Column(db.Text)
    # price = db.Column(db.String(255) )
    # meter_price = db.Column(db.String(255))
    ad_poster = db.Column(db.String(255))
    # user_id = db.Column(db.String(255))
    # ad_url = db.Column(db.String(255))
    # images = db.Column(db.Text)
    # created_time = db.Column(db.String(255))
    # last_update = db.Column(db.String(255))
    # scraped_at = db.Column(db.String(255))
    ad_type = db.Column(db.String(255))
    # street_width = db.Column(db.String(255) )
    # street_direction = db.Column(db.String(255))
    # property_age = db.Column(db.String(255) )
    # rent_period = db.Column(db.String(255) )
    # area_square_meters = db.Column(db.String(255))
    # width = db.Column(db.String(255))
    # length = db.Column(db.String(255))
    # number_apts = db.Column(db.String(255))
    # number_stores = db.Column(db.String(255))
    # number_rooms = db.Column(db.String(255))
    # number_bedrooms = db.Column(db.String(255))
    # number_living_rooms = db.Column(db.String(255))
    # number_bathrooms = db.Column(db.String(255))
    # number_kitchens = db.Column(db.String(255))
    # air_conditioning = db.Column(db.String(255))
    furnished = db.Column(db.String(255))
    # backyard = db.Column(db.String(255))
    # basement = db.Column(db.String(255))
    # car_entrance = db.Column(db.String(255))
    # driver_room = db.Column(db.String(255))
    # maid_room = db.Column(db.String(255))
    # duplex = db.Column(db.String(255))
    # extra_unit = db.Column(db.String(255))
    family = db.Column(db.String(255))
    # family_section = db.Column(db.String(255))
    number_floors = db.Column(db.String(255))
    # elevator = db.Column(db.String(255))
    stairs = db.Column(db.String(255))
    # football_stadium = db.Column(db.String(255))
    # volleyball_stadium = db.Column(db.String(255))
    # playground = db.Column(db.String(255))
    # pool = db.Column(db.String(255))
    tent = db.Column(db.String(255))
    # trees = db.Column(db.String(255))
    # wells = db.Column(db.String(255))
    # insert_date = db.Column(db.DateTime, server_default=func.now())
    # update_date = db.Column(db.DateTime, onupdate=func.now())
