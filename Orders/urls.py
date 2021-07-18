from order_app import  api
from Orders.handler import OrderCreation, HealthCheck, ScheduleOrder

api.add_resource(HealthCheck, '/')
api.add_resource(OrderCreation, '/order/create')
api.add_resource(ScheduleOrder, '/order/schedule')

# api.add_resource(OrderDetails, '/order/details')