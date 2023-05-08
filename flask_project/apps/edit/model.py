from exts import db


class ShotInfo(db.Model):
    __tablename__ = 'ShotInfo'

    id = db.Column(db.Integer, primary_key=True)
    shot = db.Column(db.Integer)
    is_follow = db.Column(db.Integer)
    user_id = db.Column(db.Integer)




class TimeInfo(db.Model):
    __tablename__ = 'TimeInfo'

    id = db.Column(db.Integer, primary_key=True)
    shot_info_id = db.Column(db.Integer)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    R = db.Column(db.LargeBinary)
    Z = db.Column(db.LargeBinary)
    P = db.Column(db.LargeBinary)
    X = db.Column(db.Text)
    y1 = db.Column(db.Text)
    y2 = db.Column(db.Text)
    y3 = db.Column(db.Text)
    y4 = db.Column(db.Text)
    y5 = db.Column(db.Text)
    p1 = db.Column(db.Float)
    p2 = db.Column(db.Float)
    p3 = db.Column(db.Float)
    p4 = db.Column(db.Float)
    p5 = db.Column(db.Float)
    p6 = db.Column(db.Float)
    p7 = db.Column(db.Float)
    p8 = db.Column(db.Float)
    p9 = db.Column(db.Float)