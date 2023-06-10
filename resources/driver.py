from flask_restful import Resource, reqparse
from models.driver import DriverModel


class Driver(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name',
                      type=str,
                      required=True,
                      help='This field cannot be left blank')

  def post(self):
    data = Driver.parser.parse_args()
    if DriverModel.find_by_attribute(name=data['name']):
        return {'message': f"A driver with name '{data['name']}' already exists."}, 400

    driver = DriverModel(name=data['name'])
    try:
      driver.save_to_db()
    except:
      return {'message': 'An error occurred inserting the driver.'}, 500

    return driver.json(), 201

  def get(self, id=None):
    if id:
        driver = DriverModel.find_by_attribute(id=id)
        if driver:
            return driver.json()
        return {'message': 'Driver not found'}, 404
    else:
        return {'drivers': [driver.json() for driver in DriverModel.query.all()]}

  def put(self, id):
    data = Driver.parser.parse_args()

    driver = DriverModel.find_by_attribute(id=id)

    if driver:
        driver.name = data['name']
        driver.save_to_db()
    else:
        return {'message': 'Driver not found.'}, 404

    return driver.json()

  def delete(self, id):
    driver = DriverModel.find_by_attribute(id=id)
    if driver:
        driver.delete_from_db()
        return {'message': 'Driver deleted.'}

    return {'message': 'Driver not found.'}, 404
