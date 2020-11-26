from app import db


# dummy table, just to see the setup is working!
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))