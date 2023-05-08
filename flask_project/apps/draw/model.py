
from exts import db

class ExprimentData(db.Model):
    __tablename__ = 'ExprimentData'

    id = db.Column(db.Integer, primary_key=True)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    data = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    update_user_id = db.Column(db.Integer)


class UserData(db.Model):
    __tablename__ = 'UserData'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    data = db.Column(db.JSON)
    update_time = db.Column(db.Time)