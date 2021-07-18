import json
import uuid
import time
from flask_restful import Resource
from flask import request, Response
from http import HTTPStatus
from order_app import db
from models import Vehicle
from settings import *


class VehicleCreation:
    """
    Class to handle vehicle data creation.
    """


    def post(self):
        msg = ''
        status_code = None
        response = {}
        data = request.get_json(force=True)
        partner_name = data.get('name', None)
        vehicle_id = data.get("vehicle_id", None)
        type = data.get('type', None)

        if not (data and partner_name and vehicle_id and type):
            msg = "Please provide all the required params. partner_name/ vehicle id/ type."
            status_code = HTTPStatus.BAD_REQUEST
            response['msg'] = msg
            return Response(json.dumps(response), status_code)

        if type not in Vehicle.ALLOWED_VEHICLE_WEIGHTS:
            msg = "Please provide valid vehicle type."
            status_code = HTTPStatus.BAD_REQUEST
            response['msg'] = msg
            return Response(json.dumps(response), status_code)

        vehicle_obj = Vehicle(vid=vehicle_id, vtype=type)
        try:
            db.session.add(vehicle_obj)
            db.session.commit()
            response['msg'] = "Vehicle created successfully."
            status_code = HTTPStatus.OK
        except Exception as err:
            response['msg'] = "Vehicle creation failed due to error: {}".format(err)
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        return Response(json.dumps(response), status_code)
