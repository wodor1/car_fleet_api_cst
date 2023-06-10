from datetime import datetime
from sqlalchemy.sql.functions import now
from db import db

class PositionModel(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car = db.relationship('CarModel')
    latitude = db.Column(db.Float(precision=5))
    longitude = db.Column(db.Float(precision=5))
    date = db.Column(db.DateTime, default=now)

    def __init__(self, car_id, latitude, longitude):
        self.car_id = car_id
        self.latitude = latitude
        self.longitude = longitude
        self.date = datetime.utcnow()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
