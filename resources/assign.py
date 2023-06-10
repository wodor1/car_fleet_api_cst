from models.car import CarModel
from models.driver import DriverModel
from flask_restful import Resource, reqparse
from db import db


class AssignDriverToCar(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('driver_id',
                      type=int,
                      required=True,
                      help='This field cannot be left blank')
  parser.add_argument('car_id',
                      type=int,
                      required=True,
                      help='This field cannot be left blank')

  def post(self):
    data = AssignDriverToCar.parser.parse_args()

    driver = DriverModel.find_by_attribute(id=data['driver_id'])

    if not driver:
      return {'message': 'Driver not found.'}, 404

    car = CarModel.find_by_attribute(id=data['car_id'])

    if not car:
      return {'message': 'Car not found.'}, 404

    if car.driver_id == driver.id:
      return {'message': 'This car is already assigned to another driver'}, 400

    other_driver = db.session.query(CarModel).filter(
        CarModel.driver_id == driver.id).first()

    if other_driver:
      return {
          'message': f"This driver is already assigned to another car"
      }, 400

    if car.driver_id is not None:
      return {'message': 'Car already has a driver.'}, 400

    car.driver_id = driver.id
    db.session.commit()

    return {
        'message':
        f"Driver {driver.name} was assigned to car: {car.license_plate}."
    }, 201

  def delete(self):
    data = AssignDriverToCar.parser.parse_args()

    driver = DriverModel.find_by_attribute(id=data['driver_id'])

    if not driver:
      return {'message': 'Driver not found.'}, 404

    car = CarModel.find_by_attribute(id=data['car_id'])

    if not car:
      return {'message': 'Car not found.'}, 404

    if car.driver_id != driver.id:
      return {'message': 'This assignment does not exist'}, 400

    car.driver_id = None
    db.session.commit()

    return {'message': f"Driver {driver.name} was unassigned from car: {car.license_plate}."}, 200
