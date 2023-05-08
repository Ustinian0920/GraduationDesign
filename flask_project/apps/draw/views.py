# coding=utf-8
from flask import jsonify,request
from flask import Blueprint
from flask_restful import Api ,Resource
from apps.common_model import XQResource
from apps.draw import control


bp  = Blueprint("draw", __name__)
api = Api(bp)

class Tree(XQResource):
    """
    树结构数据源
    """
    def post(self):
        is_ok,result = control.tree()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()


class Single(XQResource):
    """
    单张
    """
    def post(self):
        is_ok,result = control.single()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()


class Overlay(XQResource):
    """
    叠加
    """
    def post(self):
        is_ok,result = control.overlay()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()



class Waveform(XQResource):
    """
    波形
    """
    def post(self):
        is_ok,result = control.waveform()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    

class Gif(XQResource):
    """
    动画
    """
    def post(self):
        is_ok,result = control.gif()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

mapper = {
    Tree:"/draw/tree",
    Single:"/draw/single",
    Overlay:"/draw/overlay",
    Waveform:"/draw/waveform",
    Gif:"/draw/gif"
}

for k,v in mapper.items():
    api.add_resource(k,v)


