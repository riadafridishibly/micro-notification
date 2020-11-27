from datetime import datetime
from app import db


class Order(db.Model):
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    supply_id = db.Column(db.Integer, index=True, nullable=False)
    order_id = db.Column(db.String(64), nullable=False, unique=True)
    # false: CANCELLED, true: COMPLETED
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        st = 'CANCELLED'
        if self.status:
            st = 'COMPLETED'
        return f'<Order(id={self.id}, s_id={self.supply_id}, o_id={self.order_id}, status={st}, t={self.timestamp.ctime()})>'
