from datetime import datetime
from app import db

CANCELLED = False
COMPLETED = True


class Order(db.Model):
    __tablename__ = 'orders'

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
        return '<Order(i: {0}, si: {1}, oi: {2}, sts: {3}, t: {4})>'.format(
            self.id,
            self.supply_id,
            self.order_id,
            st,
            self.timestamp.ctime() if self.timestamp else None
        )
