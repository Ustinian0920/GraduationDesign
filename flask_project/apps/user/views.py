# coding=utf-8
from flask import jsonify,request
from flask import Blueprint
from flask_restful import Api ,Resource
from apps.common_model import V1Response
from apps.user import control


bp  = Blueprint("user", __name__)
api = Api(bp)

class DefectGuideList(Resource):

    def __init__(self):
        self.rep = V1Response()
    """
    绘图
    """
    def post(self):
        info = []
        
        info = control.login()
        self.rep.set_data('data', info)
        return self.rep.get_response()


api.add_resource(DefectGuideList,"/api/user/login")



