import json
import uuid
import time
from flask_restful import Resource
from flask import request, Response
from http import HTTPStatus
from order_app import db
from models import Vehicle
from settings import *


class VehicleCreation(Resource):
    """
    Class to handle vehicle data creation.
    """

    def post(self):
        response = {'msg': '', 'success': False}
        data = request.get_json(force=True)
        partner_name = data.get('name', None)
        vehicle_id = data.get("vehicle_id", None)
        type = data.get('type', None).lower()

        if not (data and partner_name and vehicle_id and type):
            msg = "Please provide all the required params. partner_name/ vehicle id/ type."
            response['msg'] = msg
            return Response(json.dumps(response), HTTPStatus.BAD_REQUEST)

        if type not in Vehicle.ALLOWED_VEHICLE_WEIGHTS:
            msg = "Please provide valid vehicle type."
            response['msg'] = msg
            return Response(json.dumps(response), HTTPStatus.BAD_REQUEST)

        vehicle_obj = Vehicle(vid=vehicle_id, vtype=type, partner_name=partner_name)
        try:
            db.session.add(vehicle_obj)
            db.session.commit()
            response['msg'] = "Vehicle created successfully."
            response['success'] = True
        except Exception as err:
            response['msg'] = "Vehicle creation failed due to error: {}".format(err)
            return Response(json.dumps(response), HTTPStatus.INTERNAL_SERVER_ERROR )

        return Response(json.dumps(response), HTTPStatus.OK)
