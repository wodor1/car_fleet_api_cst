from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from models.mixin_model import MixinModel


class FleetModel(BaseModel, MixinModel):
  __tablename__ = 'fleets'
  id = mapped_column(Integer, primary_key=True)
  name = mapped_column(String(50))

  cars = relationship('CarModel',
                      secondary='car_fleet',
                      back_populates='fleets')

  def __init__(self, name):
    self.name = name

  def json(self, include_cars=True):
    fleet = {'name': self.name, 'id': self.id}
    if include_cars:
      fleet['cars'] = [car.json(include_fleets=False) for car in self.cars]
    return fleet
