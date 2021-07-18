import json
import uuid
import time
from flask_restful import Resource
from flask import request, Response
from http import HTTPStatus
from order_app import db
from models import Order


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
            "weight": 12
        }
        :return:
        """
        order_id = str(uuid.uuid4())
        data = request.get_json(force=True)
        weight = data.get('weight', {})
        slot = data.get('slot', None)
        print("order id generated: ", order_id)

        # valid, msg = validate_order_creation_data(data)
        order_obj = Order(order_id=order_id, weight=weight)
        msg = "Order created successfully."
        resp_status = HTTPStatus.OK
        try:
            db.session.add(order_obj)
            db.session.commit()
        except Exception as err:
            msg = "Order creation failed due to error: {}".format(err)
            resp_status = HTTPStatus.INTERNAL_SERVER_ERROR

        result = {'msg': msg}

        return Response(json.dumps(result), resp_status)
