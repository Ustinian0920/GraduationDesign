from flask_sqlalchemy import SQLAlchemy
# 身份验证
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()

SHAPE_1 = 5
SHAPE_2 = 3