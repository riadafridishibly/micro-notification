from app import create_app
from app import db
from app.models import Order, COMPLETED
from flask_restful import Resource, Api
# from flask import request # to use in put request!
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


# class OrderAPI(Resource):
#     """Just to populate the database? maybe?
#     NotImplemented!
#     """

#     def put(self, supply_id):
#         ret = request.json
#         ret['supply_id'] = supply_id
#         return ret


api.add_resource(NotificationAPI, '/api/supply/<int:supply_id>')
# api.add_resource(OrderAPI, '/api/supply/<int:supply_id>')

if __name__ == '__main__':
    # TODO: use gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)


@ app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order}
