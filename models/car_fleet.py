from db import db, BaseModel
from models.mixin_model import MixinModel

class CarFleetLink(BaseModel, MixinModel):
  __tablename__ = 'car_fleet'
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), primary_key=True)
  fleet_id = db.Column(db.Integer,
                       db.ForeignKey('fleets.id'),
                       primary_key=True)

  def __init__(self, car_id, fleet_id):
    self.car_id = car_id
    self.fleet_id = fleet_id
