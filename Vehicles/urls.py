from order_app import api
from Vehicles.handler import VehicleCreation

api.add_resource(VehicleCreation, '/vehicle/create')

