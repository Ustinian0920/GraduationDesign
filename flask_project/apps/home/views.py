# coding=utf-8
from flask import jsonify,request
from flask import Blueprint
from flask_restful import Api ,Resource
from apps.common_model import XQResource
from apps.home import control


bp  = Blueprint("home", __name__)
api = Api(bp)

class CardList(XQResource):
    """
    卡片列表
    """
    def get(self):
        is_ok,result = control.card_list()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class CardInfo(XQResource):
    """
    卡片信息
    """
    def get(self):
        is_ok,result = control.card_info()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class Copy(XQResource):
    """
    拷贝
    """
    def post(self):
        is_ok,result = control.copy()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    
class CreateFlow(XQResource):
    """
    新建Flow
    """
    def post(self):
        is_ok,result = control.create_flow()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    
class CreateSub(XQResource):
    """
    新建Sub
    """
    def post(self):
        is_ok,result = control.create_sub()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()
    
    
class Update(XQResource):
    """
    编辑
    """
    def post(self):
        is_ok,result = control.update()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class Delete(XQResource):
    """
    删除
    """
    def post(self):
        is_ok,result = control.delete()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()

class ResetParam(XQResource):
    """
    恢复组件默认参数
    """
    def get(self):
        is_ok,result = control.reset_card_sub_parameters()
        if is_ok:
            self.rep.set_data("data",result)
        else:
            self.rep.set_error(result)
        return self.rep.get_response()


mapper = {
    CardList:"/home/card/list",
    CardInfo:"/home/card/info",
    Copy:"/home/card/copy",
    Update:"/home/card/update",
    Delete:"/home/card/delete",
    CreateFlow:"/home/card/create/flow",
    CreateSub:"/home/card/create/sub",
    ResetParam:"/home/card/parameters/defalt",

}

for k,v in mapper.items():
    api.add_resource(k,v)



