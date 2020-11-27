from app import create_app
from app import db
from app.models import Order
from flask_restful import Resource, Api
from flask import request

app = create_app()
api = Api(app)


class NotificationAPI(Resource):
    """Accept the supply_id, and based on this returns
    completion_rate and a message.
    """
    def get(self, supply_id):
        # add logic to calculate the completion rate
        # basically database query
        return {'message': 'Hello World', 'ID': supply_id}


class OrderAPI(Resource):
    """Just to populate the database? maybe?
    """
    def put(self, supply_id):
        ret = request.json
        ret['supply_id'] = supply_id
        return ret


api.add_resource(NotificationAPI, '/api/supply/<int:supply_id>')
api.add_resource(OrderAPI, '/api/supply/<int:supply_id>')

if __name__ == '__main__':
    # TODO: use gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order}
