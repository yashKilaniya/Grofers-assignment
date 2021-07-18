import json
import uuid
import time
from flask_restful import Resource
from flask import request, Response
from http import HTTPStatus
from order_app import db
from models import Order
from Orders.utils import validate_order_creation_data, fetch_order_details, schedule_orders, \
    deduct_available_wt_in_slot


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
        import ipdb;ipdb.set_trace()
        response = {'success': False, "msg": ''}

        # if not order_id or not isinstance(order_id, str):
        #     response['msg'] = "Please provide valid value of order id."
        #     return Response(json.dumps(response), HTTPStatus.BAD_REQUEST)
        #
        # try:
        #     success, order_obj = fetch_order_details(order_id)
        # except Exception as err:
        #     response['msg'] = "Database error occuered: err msg:{}".format(err)
        #     response['success'] = False
        #     return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        # if not success:
        #     response['msg'] = "Unable to find the given order_id:{} in DB. Please" \
        #                       "provide a valid order_id.".format(order_id)
        #     response['success'] = False
        #     return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        try:
            success, msg = schedule_orders()
        except Exception as err:
            response['msg'] = "Unable to schedule order due to error:{}".format(err)
            response['success'] = False
            return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        if not success:
            response['msg'] = "Unable to schedule order due to error:{}".format(msg)
            response['success'] = False
            return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR)

        response['msg'] = "Order scheduled successfully."
        response['success'] = True
        return Response(json.dumps(response), HTTPStatus.OK)
