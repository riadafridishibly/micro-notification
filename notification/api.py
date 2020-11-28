from app import create_app
from app import db
from app.models import Order, COMPLETED
from flask_restful import Resource, Api
from flask import request  # to use in put request!
from datetime import datetime


class Msg:
    LESS_THAN_50 = ("Your completion rate is very low."
                    " You will get suspended if you do not"
                    " increase your completion rate.")
    MORE_THAN_50 = ("Your completion rate is low."
                    " You will get less requests if you do not"
                    " increase your completionrate.")
    MORE_THAN_70 = ("Please complete more to get more requests.")


app = create_app()
api = Api(app)


def notify_dict(completion_rate_count: int):
    ret = {'completion_rate': completion_rate_count / 100}
    msg_field_name = 'message'

    if 0 <= completion_rate_count <= 50:
        ret[msg_field_name] = Msg.LESS_THAN_50
        return ret
    elif 50 < completion_rate_count <= 70:
        ret[msg_field_name] = Msg.MORE_THAN_50
        return ret
    elif 70 < completion_rate_count <= 100:
        ret[msg_field_name] = Msg.MORE_THAN_70
        return ret
    else:
        # maybe raise an exception?
        ret['completion_rate'] = 0
        ret[msg_field_name] = ""
        return ret


def get_notification(supply_id: int):
    start_of_current_day = datetime.combine(
                                datetime.utcnow(),
                                datetime.min.time())

    # how to deal with not found?
    query = Order.query.filter(Order.supply_id == supply_id).count()
    if query == 0:
        return {'status': 'Not Found'}, 404

    # check if the driver was assigned to at least 100 rides
    query = Order.query.filter(Order.supply_id == supply_id)\
        .order_by(Order.timestamp.desc())\
        .filter(Order.timestamp < start_of_current_day)\
        .count()

    if query < 100:
        # if the driver yet to be assigned 100 rides,
        # then the completion rate 0.85
        return notify_dict(85)

    query = Order.query.filter(Order.supply_id == supply_id)\
        .order_by(Order.timestamp.desc())\
        .filter(Order.timestamp < start_of_current_day)\
        .limit(100)\
        .from_self()\
        .filter(Order.status == COMPLETED)\
        .count()

    return notify_dict(query)


class NotificationAPI(Resource):
    """Accept the supply_id, and based on this returns
    completion_rate and a message.
    """

    def get(self, supply_id):
        return get_notification(supply_id)


class OrderAPI(Resource):
    """Just to populate the database? maybe?
    """

    def get(self, supply_id):
        query = Order.query.filter(Order.supply_id == supply_id).all()
        out = []
        if len(query) == 0:
            return {'message': 'Not Found'}, 404
        for o in query:
            ret = {}
            ret['id'] = o.id
            ret['status'] = o.status
            ret['supply_id'] = o.supply_id
            ret['order_id'] = o.order_id
            ret['timestamp'] = o.timestamp.ctime()
            out.append(ret)
        return out

    def post(self, supply_id):
        r = request.json
        o = Order(**r)
        param = {}

        supply_id = r.get('supply_id', None)
        try:
            int(supply_id)
        except (ValueError, TypeError):
            return dict(), 400
        param['supply_id'] = supply_id

        order_id = r.get('order_id', None)
        if not order_id:
            return dict(), 400
        param['order_id'] = str(order_id)

        status = r.get('status', None)
        try:
            bool(status)
        except (ValueError, TypeError):
            return dict(), 400
        param['status'] = bool(status)

        timestamp = r.get('timestamp', None)
        if timestamp is not None:
            timestamp = datetime.utcfromtimestamp(timestamp)
            param['timestamp'] = timestamp

        o = Order(**param)
        db.session.add(o)
        db.session.commit()

        param['timestamp'] = param['timestamp'].ctime()
        return param, 201


api.add_resource(NotificationAPI, '/api/supply/<int:supply_id>')
api.add_resource(OrderAPI, '/api/dev/supply/<int:supply_id>')


@ app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order}
