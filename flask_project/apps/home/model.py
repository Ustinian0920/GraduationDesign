from exts import db

class PrivateFlow(db.Model):
    __tablename__ = 'PrivateFlow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    struct = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    describ = db.Column(db.String(255))
    public_id = db.Column(db.Integer)
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    create_time = db.Column(db.Time)
    name = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))


class PrivateSub(db.Model):
    __tablename__ = 'PrivateSub'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    describ = db.Column(db.String(255))
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    user_id = db.Column(db.Integer)
    public_id = db.Column(db.Integer)
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    create_time = db.Column(db.Time)
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class PublicFlow(db.Model):
    __tablename__ = 'PublicFlow'

    id = db.Column(db.Integer, primary_key=True)
    struct = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    update_user_id = db.Column(db.Integer)
    describ = db.Column(db.String(255))
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    create_time = db.Column(db.Time)
    name = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class PublicSub(db.Model):
    __tablename__ = 'PublicSub'

    id = db.Column(db.Integer, primary_key=True)
    update_user_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    describ = db.Column(db.String(255))
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    create_time = db.Column(db.Time)
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))

