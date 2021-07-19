from order_app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Order(db.Model):
    """
    Model for storing Order data
    """
    __tablename__ = 'orders'

    order_id = db.Column(db.String(128), primary_key=True)
    vid = db.Column(db.String(128))
    weight = db.Column(db.Integer)
    slot = db.Column(db.Integer)
    is_scheduled = db.Column(db.Boolean, nullable=True, server_default='f')
    allowed_slots = [1, 2, 3, 4]
    # ALLOWED_MAX_WEIGHT = 100

    def __init__(self, order_id, weight, slot, vid=None):
        self.order_id = order_id
        self.weight = weight
        self.slot = slot
        self.vid = vid
        self.is_scheduled = 0


class Vehicle(db.Model):
    """
    Model for storing Vehicle data
    """
    __tablename__ = 'vehicles'

    ALLOWED_VEHICLE_WEIGHTS = {
        "bike": 30,
        "truck": 100,
        "scooter": 50
    }
    vid = db.Column(db.String(128), primary_key=True)
    vtype = db.Column(db.String(128))
    capacity = db.Column(db.Integer)
    partner_name = db.Column(db.String(128))
    orders_attached = db.Column(ARRAY(db.String))
    allowed_vehicle_weights = ALLOWED_VEHICLE_WEIGHTS

    def __init__(self, vid, vtype, partner_name):
        self.vid = vid
        self.vtype = vtype
        self.partner_name = partner_name
        if vtype not in self.allowed_vehicle_weights.keys():
            raise Exception("Vehicle Type not allowed. Can't submit vehicle data.")

        self.capacity = self.allowed_vehicle_weights.get(vtype)
        self.orders_attached = []


# class DeliveryPartner(db.Model):
#     """
#     Model for storing Delivery partner data
#     """
#     __tablename__ = 'delivery_partners'
#
#     partner_id = db.Column(db.String(128), primary_key=True)
#     partner_name = db.Column(db.String(128))
#     vid = db.Column(db.String(128))


class Slot:
    """
    Model for storing slot details.
    """
    allowed_weight = None
    remaining_weight = None

    def __init__(self):
        self.allowed_weight = 100
        self.remaining_weight = 100

    def get_remaining_wt(self):
        return self.remaining_weight


# class gg(db.Model):
#     name = db.Column(db.String,  primary_key=True)
#     orders = db.Column(ARRAY(db.String))
#
#     def __init__(self, orders):
#         self.orders = orders