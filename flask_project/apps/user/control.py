# coding=utf-8
"""
control只写业务逻辑，只能被views import
"""
from flask import request
import json
from configs.config import PROJECT_NAME, BASEDIR
from apps.user.model import User
from flask_jwt_extended import JWTManager, create_access_token


def login():
    json_data = request.get_json()

    user_name = json_data.get("user_name")
    password = json_data.get("password")

    print(f"登录收到的用户名：{user_name}")
    ####TODO
    # 去数据库查用户用户
    user = User.query.filter(User.name==user_name,User.password==password).first()
    if not user:
        return False,""
    token = create_access_token(identity=user_name)
    ####

    

    return {"token":f"Bearer {token}"}

if __name__ == "__main__":
    login()
