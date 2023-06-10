from flask_restful import Resource, reqparse
from models.car import CarModel
from flask_jwt_extended import jwt_required

class Car(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    def get(self, license_plate):
        car = CarModel.find_by_attribute(license_plate=license_plate)
        if car:
            return car.json()
        return {'message': 'Car not found'}, 404

    # license_plate is a path parameter
    def post(self, license_plate):
        if CarModel.find_by_attribute(license_plate=license_plate):
            return {
                'message': "A car with license plate '{}' already exists.".format(license_plate)
            }, 400

        if not license_plate[0:3].isalpha() or not license_plate[4:7].isdigit() or not len(license_plate) == 7:
            return {'message': 'License plate must be in Hungarian format: ABC-123'}, 400

        # data from the request body
        data = Car.parser.parse_args()
        car = CarModel(license_plate, data['type'])
        try:
            car.save_to_db()
        except:
            return {'message': 'An error occurred inserting the car.'}, 500

        return car.json(), 201

    def delete(self, license_plate):
        car = CarModel.find_by_attribute(license_plate=license_plate)
        if car:
            car.delete_from_db()
            return {'message': 'Car deleted'}

        return {'message': 'Car not found.'}, 404

    def put(self, license_plate):
        data = Car.parser.parse_args()

        car = CarModel.find_by_attribute(license_plate=license_plate)

        if car:
            car.type = data['type']
            car.save_to_db()
        else:
            return {'message': 'Car not found.'}, 404

        return car.json()


class CarList(Resource):

    @jwt_required()
    def get(self):
        return {'cars': [car.json() for car in CarModel.query.all()]}
