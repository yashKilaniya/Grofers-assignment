import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


def create_app():
    """
    Creates and configures the order creation app.
    """
    flask_app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(flask_app.instance_path)
    except OSError:
        pass
    return flask_app

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/orderdata?user=postgres&password=delhivery'
api = Api(app)
db = SQLAlchemy(app)

# url imports
from Orders.urls import *
from Vehicles.urls import *
from DeliveryPartners import *

