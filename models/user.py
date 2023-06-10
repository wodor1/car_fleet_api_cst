from models.mixin_model import MixinModel
from db import db, BaseModel
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from passlib.hash import pbkdf2_sha512

class UserModel(BaseModel, MixinModel):
  __tablename__ = 'users'
  id = mapped_column(Integer, primary_key=True)
  username = mapped_column(String(80))
  password = db.Column(db.String(800))

  def __init__(self, username, password):
    self.username = username
    self.password = password

  def json(self):
    return {'name': self.username, 'id': self.id}

  @classmethod
  def get_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()
