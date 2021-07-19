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

prod_uri = 'postgres://ynhuomatxmvtyg:da5c1923d97d6bbf4f25f0ddc9436826b614f8f515f3f4752370b0cd7946f6d0@ec2-23-21-4-7.compute-1.amazonaws.com:5432/ddigg1cu7s9bnj'
local_uri = 'postgresql://localhost/orderdata?user=postgres&password=delhivery'
app.config['SQLALCHEMY_DATABASE_URI'] = prod_uri
api = Api(app)
db = SQLAlchemy(app)

# url imports
from Orders.urls import *
from Vehicles.urls import *
from DeliveryPartners import *

