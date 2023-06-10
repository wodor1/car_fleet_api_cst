from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from models.driver import DriverModel
from models.mixin_model import MixinModel

class CarModel(BaseModel, MixinModel):
  __tablename__ = 'cars'
  id = mapped_column(Integer, primary_key=True)
  license_plate = mapped_column(String(7), unique=True)
  type = mapped_column(String(50))
  driver_id = mapped_column(Integer, ForeignKey('drivers.id'), unique=True)

  driver = relationship('DriverModel', back_populates='car', uselist=False)
  fleets = relationship('FleetModel',
                        secondary='car_fleet',
                        back_populates='cars')

  def __init__(self, license_plate, type):
    self.license_plate = license_plate
    self.type = type

  def json(self, include_fleets=True):
    driver = DriverModel.find_by_attribute(id=self.driver_id)
    car_json = {
        'license_plate': self.license_plate,
        'type': self.type,
        'car_id': self.id,
        'driver': None if driver is None else driver.json(),
    }
    if include_fleets:
      car_json['fleets'] = [
          fleet.json(include_cars=False) for fleet in self.fleets
      ]
    return car_json
