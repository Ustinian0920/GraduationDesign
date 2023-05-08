# coding=utf-8
from flask import jsonify,request
from flask import Blueprint
from flask_restful import Api ,Resource
from apps.common_model import XQResource
from apps.edit import control


bp  = Blueprint("edit", __name__)
api = Api(bp)

class FlowStruct(XQResource):
    """
    流结构
    """
    def get(self):
        is_ok,result = control.flow_struct()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    

class Run(XQResource):
    """
    运行
    """
    def post(self):
        is_ok,result = control.run()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    

class Save(XQResource):
    """
    运行
    """
    def post(self):
        is_ok,result = control.save()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    
class Log(XQResource):
    """
    日志
    """
    def get(self):
        is_ok,result = control.log()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class FlowParams(XQResource):
    """
    获取工作流参数
    """
    def get(self):
        is_ok,result = control.get_flow_params()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class UpdateFlowParams(XQResource):
    """
    编辑工作流参数
    """
    def post(self):
        is_ok,result = control.update_flow_params()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()


mapper = {
    FlowStruct:"/edit/struct",
    Run:"/edit/run",
    Save:"/edit/save",
    Log:"/edit/log",
    FlowParams:"/edit/flow/params",
    UpdateFlowParams:"/edit/flow/params/update"
}

for k,v in mapper.items():
    api.add_resource(k,v)




