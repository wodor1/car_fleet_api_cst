from flask_restful import Resource, reqparse
from models.car import CarModel
from models.car_position import PositionModel

class CarPosition(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('latitude',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('longitude',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    def post(self, id):
        car = CarModel.find_by_attribute(id=id)

        if not car:
            return {'message': 'Car not found.'}, 404

        data = CarPosition.parser.parse_args()

        car_position = PositionModel(car.id, data['latitude'], data['longitude'])
        car_position.save_to_db()

        return {'message': 'position was saved'}, 201
