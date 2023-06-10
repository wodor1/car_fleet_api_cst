from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

from models.mixin_model import MixinModel

class DriverModel(BaseModel, MixinModel):
  __tablename__ = 'drivers'
  id = mapped_column(Integer, primary_key=True)
  name = mapped_column(String(50))
  car = relationship('CarModel', back_populates='driver', uselist=False)

  def __init__(self, name):
    self.name = name

  def json(self):
    return {'name': self.name, 'id': self.id}

  @classmethod
  def find_by_attribute(cls, **kwargs):
    return cls.query.filter_by(**kwargs).first()

