# coding=utf-8
"""
control只写业务逻辑，只能被views import
"""
from flask import request
from configs.config import PROJECT_NAME, BASEDIR
import json
import numpy as np
import random
from apps.edit.model import ShotInfo,TimeInfo
from apps.home.model import PrivateFlow,PublicFlow,PrivateSub,PublicSub
from exts import db
from apps.common_control import plot_gif_frame,COLOR_LIST,STATIC_PATH
import imageio.v2 as imageio
import datetime
from flask_jwt_extended import jwt_required
from apps.common_control import get_current_user_info

# 获取工作流结构
@jwt_required()
def flow_struct() -> dict:
    is_ok = True
    err_msg = ""
    card_id = request.args.get("card_id")
    card_type = request.args.get("card_type","2")

    strcut = None

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    if card_type=="2":
        private_flow = PrivateFlow.query.filter(PrivateFlow.id==card_id,PrivateFlow.user_id==current_user_id).first()
        if private_flow:
            strcut = private_flow.struct

    return is_ok,strcut


# 运行工作流
@jwt_required()
def run() -> dict:
    is_ok = True
    err_msg = ""

    # 加载数据
    data = request.get_data()
    json_data = json.loads(data)
    shot = json_data["shot"]
    end_time = json_data.get("end_time",70)
    data = json_data.get("data")

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)



    r1 = np.linspace(-5,-3,5,dtype=np.float64)
    r2 = np.linspace(-3,-1,5,dtype=np.float64)
    r3 = np.linspace(-1,1,5,dtype=np.float64)
    r4 = np.linspace(1,3,5,dtype=np.float64)
    r5 = np.linspace(3,5,5,dtype=np.float64)
    r = np.hstack((r1,r2,r3,r4,r5))


    z1 = np.linspace(-3,-2,5,dtype=np.float64)
    z2 = np.linspace(-2,-1,5,dtype=np.float64)
    z3 = np.linspace(-1,1,5,dtype=np.float64)
    z4 = np.linspace(1,2,5,dtype=np.float64)
    z5 = np.linspace(2,3,5,dtype=np.float64)
    z = np.hstack((z1,z2,z3,z4,z5))
    R,Z = np.meshgrid(r,z)
    _R = R.tostring()
    _Z = Z.tostring()


    shot_info = ShotInfo(
        shot=shot,
        is_follow=0,
        user_id=current_user_id
    )
    db.session.add(shot_info)
    db.session.flush()

    frame_list = []
    for i,time in enumerate(range(10,end_time,10)):
        
        P = (R+random.uniform(-1,1))**2+(Z+random.uniform(-1,1))**2+random.uniform(-1,1)
        X = np.linspace(0,1,25,dtype=np.float64)
        y1 = np.random.uniform(low=3, high=8, size=25)
        y2 = np.random.uniform(low=3, high=8, size=25)
        y3 = np.random.uniform(low=3, high=8, size=25)
        y4 = np.random.uniform(low=3, high=8, size=25)
        y5 = np.random.uniform(low=3, high=8, size=25)

        _P = P.tostring()
        _X = X.tostring()
        _y1 = y1.tostring()
        _y2 = y2.tostring()
        _y3 = y3.tostring()
        _y4 = y4.tostring()
        _y5 = y5.tostring()


        p1 = time+random.uniform(-1,1)
        p2 = time/10.0+random.uniform(-0.1,0.1)
        p3 = time*10+random.uniform(-10,10)
        p4 = time+random.uniform(0,1)
        p5 = time+random.uniform(-1,0)
        p6 = time/10.0+random.uniform(-0.1,0)
        p7 = time*10+random.uniform(-10,0)
        p8 = time/10.0+random.uniform(0,0.1)
        p9 = time*10.0+random.uniform(0,10)
            
        
        time_info = TimeInfo(
            shot_info_id=shot_info.id,
            shot=shot,
            time=time,
            R=_R,Z=_Z,P=_P,
            X=_X,
            y1=_y1,y2=_y2,y3=_y3,y4=_y4,y5=_y5,
            p1=p1,p2=p2,p3=p3,p4=p4,p5=p5,p6=p6,p7=p7,p8=p8,p9=p9
        )
        db.session.add(time_info)

        ys = [y1,y2,y3,y4,y5]
        frame = plot_gif_frame(shot,time,R,Z,P,X,ys,COLOR_LIST[0])
        frame_list.append(frame)

    gif_path = f"{STATIC_PATH}/{shot}.gif"
    
    if len(frame_list) > 1:
        print("生成gif...")
        imageio.mimsave(gif_path, frame_list, 'GIF', duration=0.2)  
    db.session.commit()


    return is_ok,err_msg

# 保存工作流
@jwt_required()
def save() -> dict:
    is_ok = True
    err_msg = ""

    # 加载数据
    json_data = request.get_json()
    current_time = datetime.datetime.now()

    id = json_data["id"]
    data = json.loads(json_data.get("data"))
    node_list = data.get("nodeList",[])

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    if id==0:
        private_flow = PrivateFlow(
            update_time=current_time,
            create_time=current_time,
            name="Undefined",
            parameters={},
            user_id=current_user_id,
            describ="新创建的工作流"
        )
        db.session.add(private_flow)
        db.session.flush()
        db.session.commit()
        id = private_flow.id

    params = {}

    q_private_flow = PrivateFlow.query.filter(PrivateFlow.id==id,PrivateFlow.user_id==current_user_id)
    if q_private_flow.first():
        params = q_private_flow.first().parameters
    
    for node in node_list:
        if node.get("id") in ["nodeStart","nodeEnd"]:
            continue
        private_sub_id = node.get("id")
        private_sub = PrivateSub.query.filter(PrivateSub.id==private_sub_id,PrivateSub.user_id==current_user_id).first()
        if private_sub:
            params[str(private_sub_id)] = private_sub.parameters



    update_dic = {
        "struct":data,
        "parameters":params
    }

    print(id)

    
    q_private_flow.update(update_dic)


    return is_ok,data

# 运行日志
@jwt_required()
def log() -> str:
    is_ok = True
    err_msg = ""

    json_data = request.args

    line = int(json_data.get("line",1000))
    print(line)

    log_path = f"{STATIC_PATH}/log.txt"
    with open(log_path,"r") as f:
        line_list = f.readlines(line)
        log_str = "".join(line_list)

    return is_ok,log_str

# 获取工作流的参数
@jwt_required()
def get_flow_params():
    is_ok = True
    err_msg = ""

    json_data = request.args

    flow_id = json_data.get("flow_id")
    card_type = json_data.get("card_type","2")
    private_sub_id = json_data.get("private_sub_id")
    public_sub_id = json_data.get("public_sub_id")

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    params = {}

    private_flow = PrivateFlow.query.filter(PrivateFlow.id==flow_id,PrivateFlow.user_id==current_user_id).first()
    if private_flow:
        params = private_flow.parameters.get(private_sub_id)
    if not params:
        private_sub =  PrivateSub.query.filter(PrivateSub.id==private_sub_id,PrivateSub.user_id==current_user_id).first()
        if private_sub:
            params = private_sub.parameters
        else:
            public_sub = PublicSub.query.filter(PublicSub.id==public_sub_id).first()
            if public_sub:
                params = public_sub.parameters
           

    return is_ok,params

# 编辑工作流的参数
@jwt_required()
def update_flow_params():
    is_ok = True
    err_msg = ""

    json_data = request.get_json()

    flow_id = json_data.get("flow_id")
    card_type = json_data.get("card_type",2)
    sub_id = json_data.get("sub_id")
    params_dic = json_data.get("params_dic")

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    if card_type==2:
        q_private_flow = PrivateFlow.query.filter(PrivateFlow.id==flow_id,PrivateFlow.user_id==current_user_id)
        if q_private_flow.first():
            parameters = q_private_flow.first().parameters
            parameters[str(sub_id)] = params_dic
            update_dic = {"parameters":parameters}
            q_private_flow.update(update_dic)


    return is_ok,err_msg


if __name__ == "__main__":
    ...

