from datetime import datetime
from sqlalchemy.sql.functions import now
from db import db
import requests

class PositionModel(db.Model):
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    car = db.relationship('CarModel', backref='positions')
    latitude = db.Column(db.Float(precision=5))
    longitude = db.Column(db.Float(precision=5))
    address = db.Column(db.String(300))  # új oszlop
    date = db.Column(db.DateTime, default=now)

    @staticmethod
    def resolve_address(latitude, longitude):
        response = requests.get('https://nominatim.openstreetmap.org/reverse', params={
            'lat': latitude,
            'lon': longitude,
            'format': 'json'
        })

        if response.status_code != 200:
            return ''

        data = response.json()
        return data.get('display_name', '')

    def __init__(self, car_id, latitude, longitude):
        self.car_id = car_id
        self.latitude = latitude
        self.longitude = longitude
        self.address = self.resolve_address(latitude, longitude)
        self.date = datetime.utcnow()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'car_id': self.car_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,  # include in the json response
            'date': self.date.isoformat()
        }
