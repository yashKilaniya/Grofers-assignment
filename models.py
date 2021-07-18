from order_app import db
from settings import ALLOWED_VEHICLE_WEIGHTS


class Order(db.Model):
    """
    Model for storing Order data
    """
    __tablename__ = 'orders'

    order_id = db.Column(db.String(128), primary_key=True)
    vid = db.Column(db.String(128))
    weight = db.Column(db.Integer)

    def __init__(self, order_id, weight, vid=None):
        self.order_id = order_id
        self.vid = vid
        self.weight = weight


class Vehicle(db.Model):
    """
    Model for storing Vehicle data
    """
    __tablename__ = 'vehicles'
    vid = db.Column(db.String(128), primary_key=True)
    type = db.Column(db.String(128))
    capacity = db.Column(db.Integer)
    allowed_vehicle_weights = ALLOWED_VEHICLE_WEIGHTS

    def __init__(self, vid, vtype):
        self.vid = vid
        self.vtype = vtype


class DeliveryPartner(db.Model):
    """
    Model for storing Delivery partner data
    """
    __tablename__ = 'delivery_partners'
    parter_id = db.Column(db.String(128), primary_key=True)
    partner_name = db.Column(db.String(128))
    vid = db.Column(db.String(128))