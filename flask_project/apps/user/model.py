from exts import db



class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Integer, info='管理员权限 0普通用户 1管理员')


