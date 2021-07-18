from order_app import  api
from Orders.handler import OrderCreation, HealthCheck

api.add_resource(HealthCheck, '/')
api.add_resource(OrderCreation, '/order/create')

# api.add_resource(OrderDetails, '/order/details')