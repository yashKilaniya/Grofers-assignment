import json
import uuid
import time
from flask_restful import Resource
from flask import request, Response
from http import HTTPStatus
from order_app import db
from models import *
from sqlalchemy import desc
from Orders.utils import validate_order_creation_data, fetch_order_details, \
    deduct_available_wt_in_slot, update_vid_on_orders, get_total_weight_of_slot


class HealthCheck(Resource):
    """"
    Health Check API.
    """
    def get(self):
        return "Health OK."


class OrderCreation(Resource):
    """
    API for order creation.
    """

    def post(self):
        """
        {
            "weight": 12,
            "slot": 1/2/3/4
        }
        :return:
        """
        order_id = str(uuid.uuid4())
        data = request.get_json(force=True)
        response = {}
        valid, msg = validate_order_creation_data(data)
        if not valid:
            response['msg'] = msg
            response['success'] = False
            return Response(json.dumps(response), HTTPStatus.BAD_REQUEST)

        weight = data.get('weight', {})
        slot = data.get('slot', None)

        order_obj = Order(order_id, weight, slot)
        try:
            db.session.add(order_obj)
            db.session.commit()
        except Exception as err:
            response['msg'] = "Order creation failed due to error: {}".format(err)
            response['success'] = False
            return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        # deduct the given wt from the available amount.
        deduct_available_wt_in_slot(weight, slot)
        response['msg'] = "Order created successfully."
        response['success'] = True
        return Response(json.dumps(response), HTTPStatus.OK)


class ScheduleOrder(Resource):
    """
    API for scheduling the orders and attaching the orders to the vehicles.
    """
    def patch(self):
        response = {'success': False, "msg": '', 'data': {}}

        try:
            slot1_data = ScheduleOrder.schedule_orders(slot=1,
                                                       allowed_vehicles = {"bike": 3, "scooter": 2})
            slot2_data = ScheduleOrder.schedule_orders(slot=2,
                                                       allowed_vehicles = {"truck":1, "bike": 3, "scooter": 2})
            slot3_data = ScheduleOrder.schedule_orders(slot=3,
                                                       allowed_vehicles = {"truck":1, "bike": 3, "scooter": 2})
            slot4_data = ScheduleOrder.schedule_orders(slot=4,
                                                       allowed_vehicles = {"truck":1})
        except Exception as err:
            response['msg'] = "Unable to schedule order due to error:{}".format(err)
            response['success'] = False
            return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        # if not (slot1_data and slot2_data and slot3_data and slot4_data):
        #     response['msg'] = "Unable to schedule order due to error:{}".format(msg)
        #     response['success'] = False
        #     return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        response['msg'] = "Order scheduled successfully."
        response['success'] = True
        response['data'] = {
            'slot1_details': slot1_data,
            'slot2_details': slot2_data,
            'slot3_details': slot3_data,
            'slot4_details': slot4_data
        }
        return Response(json.dumps(response), HTTPStatus.OK)

    @staticmethod
    def schedule_orders(slot, allowed_vehicles):
        # from Orders import slot1, slot2, slot3, slot4

        data = []
        if slot == 4:
            try:
                slot_4_orders = db.session.query(Order).filter(Order.slot == 4).filter(Order.is_scheduled == 'f').all()
                truck = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'truck').first()

                if slot_4_orders and truck:
                    data = update_vid_on_orders(slot_4_orders, truck)
                return data
            except Exception as err:
                raise Exception("Unable to fetch slot 4 orders dur to error:{}".format(err))

        elif slot == 1:
            # Fetching the orders in decreasing amount of weights from DB.
            slot1_orders = db.session.query(Order).filter(Order.slot == 1).\
                filter(Order.is_scheduled == 'f').order_by(desc(Order.weight)).all()
            total_amount = get_total_weight_of_slot(slot1_orders)

            vehicles = {}
            if 0 < total_amount <= 30:
                vehicles.update({'bike': 1})
            elif 30 < total_amount <= 50:
                vehicles.update({'scooter': 1})
            elif 50 < total_amount <= 60:
                vehicles.update({'bike': 2})
            elif 60 < total_amount <= 80:
                vehicles.update({'bike': 1, 'scooter': 1})
            elif 80 < total_amount <= 100:
                vehicles.update({'scooter': 2})

            data = []
            Vehicles = []
            DATA = {}
            if vehicles.get('scooter'):
                Scooters = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'scooter').limit(vehicles.get('scooter')).all()
                for scooter in Scooters:
                    Vehicles.append([scooter, 50])

            if vehicles.get('bike'):
                Bikes = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'bike').limit(vehicles.get('bike')).all()
                for bike in Bikes:
                    Vehicles.append([bike, 30])

            for order in slot1_orders:
                for vehicle in Vehicles:
                    if order.weight <= vehicle[1]:
                        if not DATA.get(vehicle[0]):
                            DATA[vehicle[0]] = []
                        DATA[vehicle[0]].append(order)
                        vehicle[1] -= order.weight

                        order.vid = vehicle[0].vid
                        order.is_scheduled = True
                        try:
                            db.session.commit()
                            # order_data['list_order_ids_assigned'].append(order.order_id)
                        except Exception as err:
                            raise Exception("Error occurred while scheduling the orders. ERROR:{}".format(err))

            # Prepare the response.
            for vehicle, orders in DATA.items():
                order_data = {
                    "vehicle_type": vehicle.vtype,
                    "delivery_partner_name": vehicle.partner_name,
                    "list_order_ids_assigned": [order.order_id for order in orders]
                }
                data.append(order_data)

            return data

        elif slot == 2 or slot == 3:
            # Fetching the orders in decreasing amount of weights from DB.
            slot_2_3_orders = db.session.query(Order).filter(Order.slot == slot).\
                filter(Order.is_scheduled == 'f').order_by(desc(Order.weight)).all()
            total_amount = get_total_weight_of_slot(slot_2_3_orders)

            vehicles = {}
            if 0 < total_amount <= 30:
                vehicles.update({'bike': 1})
            elif 30 < total_amount <= 50:
                vehicles.update({'scooter': 1})
            elif 50 < total_amount <= 60:
                vehicles.update({'bike': 2})
            elif 60 < total_amount <= 80:
                vehicles.update({'bike': 1, 'scooter': 1})
            elif 80 < total_amount <= 100:
                vehicles.update({'truck': 1})

            data = []
            Vehicles = []
            DATA = {}
            if vehicles.get('scooter'):
                Scooters = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'scooter').limit(vehicles.get('scooter')).all()
                for scooter in Scooters:
                    Vehicles.append([scooter, 50])

            if vehicles.get('bike'):
                Bikes = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'bike').limit(vehicles.get('bike')).all()
                for bike in Bikes:
                    Vehicles.append([bike, 30])

            if vehicles.get('truck'):
                Truck = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                    Vehicle.vtype == 'truck').limit(vehicles.get('truck')).all()
                for truck in Truck:
                    Vehicles.append([truck, 100])

            for order in slot_2_3_orders:
                for vehicle in Vehicles:
                    if order.weight <= vehicle[1]:
                        if not DATA.get(vehicle[0]):
                            DATA[vehicle[0]] = []
                        DATA[vehicle[0]].append(order)
                        vehicle[1] -= order.weight

                        order.vid = vehicle[0].vid
                        order.is_scheduled = True
                        try:
                            db.session.commit()
                        except Exception as err:
                            raise Exception("Error occurred while scheduling the orders. ERROR:{}".format(err))


            # Prepare the response.
            for vehicle, orders in DATA.items():
                order_data = {
                    "vehicle_type": vehicle.vtype,
                    "delivery_partner_name": vehicle.partner_name,
                    "list_order_ids_assigned": [order.order_id for order in orders]
                }
                data.append(order_data)

            return data






        total_amount = get_total_weight_of_slot(slot_4_orders)
        if total_amount and allowed_vehicles.get('truck'):
            truck = db.session.query(Vehicle).filter(Vehicle.orders_attached == '{}').filter(
                Vehicle.vtype == 'truck').first()
            if truck:
                allowed_vehicles['truck'] = 0
                update_vid_on_orders(slot_4_orders, truck.vid, vtype, data)
                data = update_response(orders)
            else:
                print("No orders can be served in slot 4 today.")

        try:
            slot_4_orders = db.session.query(Order).filter(Order.slot == 4).filter(Order.is_scheduled == 'f').all()
        except Exception as err:
            raise Exception("Unable to fetch slot 4 orders dur to error:{}".format(err))
