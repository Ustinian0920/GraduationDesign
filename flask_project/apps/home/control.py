# coding=utf-8
"""
control只写业务逻辑，只能被views import
"""
from flask import request
import json
from configs.config import PROJECT_NAME, BASEDIR
from apps.home.model import PrivateFlow,PrivateSub,PublicFlow,PublicSub
from exts import db
import datetime
from apps.common_utils import time_to_str
from flask_jwt_extended import jwt_required
from apps.common_control import get_current_user_info
from apps.edit.model import TimeInfo

# 获取卡片列表
@jwt_required()
def card_list() -> list:
    is_ok = True
    err_msg = ""
    # 加载数据
    json_data = request.args

    card_type = int(json_data.get("card_type"))

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)
  
    current_time = datetime.datetime.now()

    q = None
    if card_type==1:
        q = PrivateSub.query.filter(current_user_id==PrivateSub.user_id).order_by()
    elif card_type==2:
        q = PrivateFlow.query.filter(current_user_id==PrivateFlow.user_id)
    elif card_type==3:
        q = PublicSub.query.filter()
    elif card_type==4:
        q = PublicFlow.query.filter()
       

    rows = q.all()
    card_list = []
    for i,row in enumerate(rows):
        dic = {}
        dic["card_id"] = row.id
        dic["card_name"] = row.name
        dic["card_describ"] = row.describ
        dic["index"] = i
        card_list.append(dic)

    return is_ok,card_list

# 获取卡片信息
@jwt_required()
def card_info():
    is_ok = True
    err_msg = ""
    # 加载数据
    json_data = request.args

    card_type = int(json_data.get("card_type"))
    card_id = int(json_data.get("card_id"))

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)
    current_time = datetime.datetime.now()
    row = None
    dic = {"info":{}}
    if card_type==1:
        q = PrivateSub.query.filter(current_user_id==PrivateSub.user_id,card_id==PrivateSub.id)
    elif card_type==2:
        q = PrivateFlow.query.filter(current_user_id==PrivateFlow.user_id,card_id==PrivateFlow.id)
        dic["info"]["struct"] = q.first().struct
    elif card_type==3:
        q = PublicSub.query.filter(card_id==PublicSub.id)
    elif card_type==4:
        q = PublicFlow.query.filter(card_id==PublicFlow.id)
        dic["info"]["struct"] = q.first().struct
        
    row = q.first()
    dic["info"] = {
        "id":row.id,
        "card_type":card_type,
        "name":row.name,
        "describ":row.describ,
        "author":row.author,
        "language":row.language.split(","),
        "parameters":row.parameters,
        "update_time":time_to_str(row.update_time),
        "create_time":time_to_str(row.create_time),
        "equipment":row.equipment,
        "department":row.department,
        "program":row.program,
        "output":row.output
        
    }

    return is_ok,dic

# 创建Flow
@jwt_required()
def create_flow():
    is_ok = True
    err_msg = ""

    json_data = request.get_json()

    name = json_data.get("name")
    describ = json_data.get("describ")
    parameters = json_data.get("parameters")
    language = json_data.get("language")
    author = json_data.get("author")
    equipment = json_data.get("equipment")
    department = json_data.get("department")
    program = json_data.get("program")
    output = json_data.get("output")

    current_time = datetime.datetime.now()

    public_flow = PublicFlow(
        name=name,
        describ=describ,
        parameters=parameters,
        language=language,
        author=author,
        create_time=current_time,
        update_time=current_time,
        equipment = equipment,
        department = department,
        program = program,
        output = output
    )

    db.session.add(public_flow)
    db.session.commit()

    return is_ok,err_msg

# 创建Sub
@jwt_required()
def create_sub():
    is_ok = True
    err_msg = ""

    json_data = request.get_json()

    name = json_data.get("name")
    describ = json_data.get("describ")
    parameters = json_data.get("parameters")
    language = json_data.get("language")
    author = json_data.get("author")
    equipment = json_data.get("equipment")
    department = json_data.get("department")
    program = json_data.get("program")
    output = json_data.get("output")

    current_time = datetime.datetime.now()

    public_flow = PublicSub(
        name=name,
        describ=describ,
        parameters=parameters,
        language=language,
        author=author,
        create_time=current_time,
        update_time=current_time,
        equipment = equipment,
        department = department,
        program = program,
        output = output
    )

    db.session.add(public_flow)
    db.session.commit()

    return is_ok,err_msg

# 组件参数恢复默认值
@jwt_required()
def reset_card_sub_parameters():
    is_ok = True
    err_msg = ""

    # 加载数据
    json_data = request.args

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    # card_id = json_data.get("card_id")

    # q = PrivateSub.query.filter(card_id==PrivateSub.id)
    # public_id = q.first().public_id
    # parameters = PublicSub.query.filter(public_id==PublicSub.id).first().parameters

    # current_time = datetime.datetime.now()
    # q.update({"parameters":parameters,"update_time":current_time})

    rows_time_info = TimeInfo.query.filter().order_by(TimeInfo.time,TimeInfo.id).all()
    result_list = []
    for row_time_info in rows_time_info:
        dic = {
            "id":row_time_info.id,
            "time":row_time_info.time
        }
        result_list.append(dic)

    return is_ok,result_list

# 拷贝公共卡片到本地
@jwt_required()
def copy():
    is_ok = True
    err_msg = ""
    # 加载数据
    json_data = request.get_json()

    card_type = json_data.get("card_type")
    card_id = json_data.get("card_id")

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)
    current_time = datetime.datetime.now()

    # sub
    if card_type==3:
        public = PublicSub.query.filter(card_id==PublicSub.id).first()
        private = PrivateSub(
            name = public.name,
            user_id = current_user_id,
            parameters = public.parameters,
            update_time = current_time,
            create_time = current_time,
            describ = public.describ,
            public_id = public.id,
            language = public.language,
            author = public.author,
            equipment = public.equipment,
            department = public.department,
            program = public.program,
            output = public.output
        )
    # flow
    elif card_type==4:
        public = PublicFlow.query.filter(card_id==PublicFlow.id).first()
        private = PrivateFlow(
            name = public.name,
            user_id = current_user_id,
            struct = public.struct,
            parameters = public.parameters,
            update_time = current_time,
            create_time = current_time,
            describ = public.describ,
            public_id = public.id,
            language = public.language,
            author = public.author,
            equipment = public.equipment,
            department = public.department,
            program = public.program,
            output = public.output
        )

    db.session.add(private)
    db.session.commit()


    return is_ok,err_msg

# 编辑
@jwt_required()
def update() -> dict:
    is_ok = True
    err_msg = ""
    # 加载数据
    json_data = request.get_json()
    
    card_type = json_data.get("card_type")
    card_id = json_data.get("card_id")
    card_name = json_data.get("name")
    describ = json_data.get("describ")
    parameters = json_data.get("parameters")
    author = json_data.get("author")
    languege = json_data.get("languege")
    struct = json_data.get("struct")
    equipment = json_data.get("equipment")
    department = json_data.get("department")
    program = json_data.get("program")
    output = json_data.get("output")

   
    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)
    current_time = datetime.datetime.now()

    q = None

    if card_type==1:
        q = PrivateSub.query.filter(current_user_id==PrivateSub.user_id,card_id==PrivateSub.id)
        if parameters:
            update_dic = {
                "parameters":parameters,
                "update_time":current_time,
            }
        else:
            update_dic = {
                "name":card_name,
                "author":author,
                "describ":describ,
                "update_time":current_time,
                "equipment":equipment,
                "department":department,
                "program":program,
                "output":output
            }

    elif card_type==2:
        q = PrivateFlow.query.filter(current_user_id==PrivateFlow.user_id,card_id==PrivateFlow.id)
        if struct:
            update_dic = {
                "struct":struct,
                "update_time":current_time,
                "parameters":parameters
            }
            
        else:
            update_dic = {
                "name":card_name,
                "describ":describ,
                "update_time":current_time,
                "equipment":equipment,
                "department":department,
                "program":program,
                "output":output
            }
            

    elif card_type==3:
        q = PublicSub.query.filter(card_id==PublicSub.id)
        update_dic = {
            "name":card_name,
            "describ":describ,
            "parameters":parameters,
            "update_time":current_time,
            "author":author,
            "languege":languege,
            "equipment":equipment,
            "department":department,
            "program":program,
            "output":output
        }
    elif card_type==4:
        q = PublicFlow.query.filter(card_id==PublicFlow.id)
        update_dic = {
            "name":card_name,
            "describ":describ,
            "parameters":parameters,
            "update_time":current_time,
            "struct":struct,
            "author":author,
            "languege":languege,
            "equipment":equipment,
            "department":department,
            "program":program,
            "output":output
        }

    q.update(update_dic)

    update_dic = {
        "is_ok":True
    }

    return is_ok,err_msg

# 删除
@jwt_required()
def delete() -> dict:
    is_ok = True
    err_msg = ""
    # 加载数据
    json_data = request.get_json()

    
    card_type = json_data.get("card_type")
    card_id = json_data["card_id"]

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    if card_type==1:
        q = PrivateSub.query.filter(current_user_id==PrivateSub.user_id,card_id==PrivateSub.id)
    elif card_type==2:
        q = PrivateFlow.query.filter(current_user_id==PrivateFlow.user_id,card_id==PrivateFlow.id)
    elif card_type==3:
        q = PublicSub.query.filter(card_id==PublicSub.id)
        PrivateSub.query.filter(card_id==PrivateSub.public_id).delete()
    elif card_type==4:
        q = PublicFlow.query.filter(card_id==PublicFlow.id)
        PrivateFlow.query.filter(card_id==PrivateFlow.public_id).delete()


    if q.first():
            q.delete()
    delete_dic = {
        "is_ok":True,
        "card_type":card_type,
        "id":id
    }

    return is_ok,err_msg

if __name__ == "__main__":
    ...
