from models import Order
from order_app import db


def validate_order_creation_data(data):
    """
    Validates the input for the order creation.
    """
    weight = data.get('weight', {})
    slot = data.get('slot', None)

    if not (data and weight and slot):
        return False, "Please provide the required details. weight/slot"

    if slot not in Order.allowed_slots:
        return False, "Invalid slot passed. Please try again with a valid slot."

    attached_slot = get_slot_model(slot)
    remaining_slot_weight = attached_slot.remaining_weight
    if weight > remaining_slot_weight:
        return False, "Maximum weight limit for the slot has reached. You can order tomorrow!!"

    return True, "Valid data received."


def fetch_order_details(order_id):
    """
    FN to fetch the details of given order_id from the DB.
    """
    if not order_id:
        return False, None

    order_details = db.session.query(Order).filter(Order.order_id == order_id).first()
    return True, order_details


def update_vid_on_orders(orders, vehicle):
    data = []
    order_data = {
                    'vehicle_type': vehicle.vtype,
                    'delivery_partner_name': vehicle.partner_name,
                    'list_order_ids_assigned': []
                 }
    for order in orders:
        order = Order.query.filter_by(order_id=order.order_id).first()
        order.vid = vehicle.vid
        order.is_scheduled = True
        try:
            db.session.commit()
            order_data['list_order_ids_assigned'].append(order.order_id)
        except Exception as err:
            raise Exception("Error occurred while scheduling the orders. ERROR:{}".format(err))
    data.append(order_data)
    return data


def update_vid_on_slot_orders(order, vehicle, data):
    order_data = {
                    'vehicle_type': vehicle.vtype,
                    'delivery_partner_name': vehicle.partner_name,
                    'list_order_ids_assigned': []
                 }
    for order in orders:
        order = Order.query.filter_by(order_id=order.order_id).first()
        order.vid = vehicle.vid
        order.is_scheduled = True
        try:
            # db.session.commit()
            order_data['list_order_ids_assigned'].append(order.order_id)
        except Exception as err:
            raise Exception("Error occurred while scheduling the orders. ERROR:{}".format(err))
    data.append(order_data)
    return data


def get_total_weight_of_slot(orders):
    total_weight = 0
    for order in orders:
        total_weight += order.weight
    return total_weight


def get_slot_model(slot):
    """
    return appropriate slot model for the slot provided in the order creation api.
    """
    from Orders import slot1, slot2, slot3, slot4
    if slot == 1:
        return slot1
    if slot == 2:
        return slot2
    if slot == 3:
        return slot3
    if slot == 4:
        return slot4


def deduct_available_wt_in_slot(weight, slot):
    """
    Deducts the amount of provided weight from the available weight of
    a particular slot.
    """
    attached_slot = get_slot_model(slot)
    attached_slot.remaining_weight -= weight
