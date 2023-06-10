from flask_restful import Resource
from models.fleet import FleetModel

class Fleet(Resource):

  def post(self, name):
    if FleetModel.find_by_attribute(name=name):
      return {'message': f'A fleet with name {name} already exists.'}, 400

    fleet = FleetModel(name)
    try:
      fleet.save_to_db()
    except:
      return {'message': 'An error occurred inserting the fleet.'}, 500

    return fleet.json(), 201

  def get(self, name):
    fleet = FleetModel.find_by_attribute(name=name)
    if fleet:
      return fleet.json()
    return {'message': 'Fleet not found'}, 404

  def delete(self, name):
    fleet = FleetModel.find_by_attribute(name=name)
    if fleet:
      fleet.delete_from_db()
      return {'message': 'Fleet deleted'}

    return {'message': 'Fleet not found.'}, 404

  def put(self, name):
    data = Fleet.parser.parse_args()

    fleet = FleetModel.find_by_attribute(name=name)

    if fleet:
      fleet.name = data['name']
      fleet.save_to_db()
    else:
      return {'message': 'Fleet not found.'}, 404

    return fleet.json()

class FleetList(Resource):

  def get(self):
    return {'fleets': [fleet.json() for fleet in FleetModel.query.all()]}
