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

prod_uri = 'postgres://inflxwwhowsddy:719571319eea9ba99313058b6944d053db23f17f89950a8609da27d8b70f8d35@ec2-52-23-40-80.compute-1.amazonaws.com:5432/dcprc1luuru0ve'
local_uri = 'postgresql://localhost/orderdata?user=postgres&password=delhivery'
app.config['SQLALCHEMY_DATABASE_URI'] = prod_uri
api = Api(app)
db = SQLAlchemy(app)

# url imports
from Orders.urls import *
from Vehicles.urls import *
from DeliveryPartners import *

