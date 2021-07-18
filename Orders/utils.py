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


def schedule_orders():
    from Orders import slot1, slot2, slot3, slot4
    allowed_vehicles = {
        "truck" : 1,
        "bike": 3,
        "scooter": 2
    }
    import ipdb;ipdb.set_trace()

    response = {'msg': '', 'success': '', 'data': {}}
    data = []
    try:
        slot_4_orders = db.session.query(Order).filter(Order.slot==4).filter(Order.is_scheduled=='f').all()
    except Exception as err:
        raise Exception("Unable to fetch slot 4 orders dur to error:{}".format(err))

    total_amount = get_total_weight_of_slot(slot_4_orders)
    if total_amount and allowed_vehicles.get('truck'):
        truck = db.session.query(Vehicle).filter(Vehicle.orders_attached=='{}').filter(
            Vehicle.vtype=='truck').first()
        if truck:
            allowed_vehicles['truck'] = 0
            update_vid_on_orders(slot_4_orders, truck.vid, vtype, data)
            data = update_response(orders)
        else:
            print("No orders can be served in slot 4 today.")



    try:
        slot_4_orders = db.session.query(Order).filter(Order.slot==4).filter(Order.is_scheduled=='f').all()
    except Exception as err:
        raise Exception("Unable to fetch slot 4 orders dur to error:{}".format(err))


def update_vid_on_orders(orders, vid, vtype, data):
    order_data = {'vehicle_type': None, 'delivery_partner_id': vid, 'list_order_ids_assigned':[]}
    for order in orders:
        order = Order.query.filter_by(order_id=order.order_id).first()
        order.vid = vid
        order.is_scheduled = True
        try:
            db.session.commit()
            order_data['vehicle_type'] = vtype
            order_data['list_order_ids_assigned'].extend(order.order_id)
            data.append(order_data)
        except Exception as err:
            raise Exception("Error occurred while scheduling the orders. ERROR:{}".format(err))


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
