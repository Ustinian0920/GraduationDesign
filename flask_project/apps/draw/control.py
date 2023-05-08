# coding=utf-8
"""
control只写业务逻辑，只能被views import
"""
from flask import request
import json
from configs.config import PROJECT_NAME, BASEDIR
from apps.edit.model import TimeInfo,ShotInfo
from apps.common_control import plot_background,plot_contour,plot_overlay,plot_param,\
    plot_waveform,MyEncoder,single_data_from_sql,COLOR_LIST,param_y_limit,STATIC_PATH,\
    get_wave_fig
import numpy as np
from exts import SHAPE_1,SHAPE_2
from io import BytesIO
import base64
import matplotlib
from exts import db
import os
from flask_jwt_extended import jwt_required
from apps.common_control import get_current_user_info
matplotlib.use('Agg')

# 获取shot time的目录结构
@jwt_required()
def tree() -> dict:
    is_ok = True
    err_msg = ""

    json_data = request.get_json()
    plot_type = json_data.get("plot_type","efit")
    is_follow = json_data.get("is_follow",0)

    current_user = get_current_user_info()
    current_user_id = current_user.get("id",1)

    dic = {}
    rows_shot_info = ShotInfo.query.filter(ShotInfo.is_follow==is_follow,ShotInfo.user_id==current_user_id).all()
    for row_shot_info in rows_shot_info:
        shot = row_shot_info.shot
        shot_info_id = row_shot_info.id
        dic[shot] = []
        rows_time_info = TimeInfo.query.filter(TimeInfo.shot_info_id==shot_info_id).all()
        for row_time_info in rows_time_info:
            dic[shot].append(row_time_info.time)

    result_list = []
    if plot_type in ["efit","overlay"]:
        for k,v in dic.items():
            tem_dic = {"label":str(k),"children":[{"label":str(i)} for i in v]}
            result_list.append(tem_dic)
    else:
        for k in dic.keys():
            tem_dic = {"label":str(k)}
            result_list.append(tem_dic)
    return is_ok,result_list


# 绘制单张图
@jwt_required()
def single() -> str:
    is_ok = True
    err_msg = ""

    # 加载数据
    data = request.get_data()
    json_data = json.loads(data)
    
    shot = json_data["shot"]
    time = json_data["time"]
    is_follow = json_data.get("is_follow",0)

    # 获取绘图数据
    row_shot_info = ShotInfo.query.filter(ShotInfo.shot==shot,ShotInfo.is_follow==is_follow).first()
    if row_shot_info:
        shot_info_id = row_shot_info.id
        row_time_info = TimeInfo.query.filter(TimeInfo.shot_info_id==shot_info_id,TimeInfo.time==time).first()
        if row_time_info:
            R,Z,P,X,ys = single_data_from_sql(row_time_info)

    # 绘制背景
    fig,axs = plot_background()
    # 绘制等高图
    plot_contour(axs[0],R,Z,P)
    # 绘制参数图
    plot_param(axs[1:],X,ys,COLOR_LIST[0])
    # 固定参数图的高度
    param_y_limit(axs[1:])
    title = f"Shot:{shot} Time:{time}"
    axs[1].set_title(title)
    # 保存到内存里
    file = BytesIO()
    fig.savefig(file,format="png",bbox_inches = 'tight')
    # 从内存中读出图像数据转为json字符串
    file.seek(0)
    dic = base64.b64encode(file.read())
    data_json_str = json.dumps(dic,cls=MyEncoder).strip("\"")

    return is_ok,data_json_str


# 绘制叠加图
@jwt_required()
def overlay() -> str:
    is_ok = True
    err_msg = ""

    # 加载数据
    data = request.get_data()
    json_data = json.loads(data)
    
    time_list = json_data["time_list"]
    is_follow = json_data.get("is_follow",0)

    mapper = {"10":"124","20":"125","30":"126"}

    datas = []
    for time in time_list:
        dic = {}
        dic["shot"] = mapper.get(time,"124")
        dic["time"] = time
        datas.append(dic)

    fig,axs = plot_background()
    for i,data in enumerate(datas):
        shot = data["shot"]
        time = data["time"]
        row_shot_info = ShotInfo.query.filter(ShotInfo.shot==shot,ShotInfo.is_follow==is_follow).first()
        if row_shot_info:
            shot_info_id = row_shot_info.id
            row_time_info = TimeInfo.query.filter(TimeInfo.shot_info_id==shot_info_id,TimeInfo.time==time).first()
            if row_time_info:
                color = COLOR_LIST[i%len(COLOR_LIST)]
                R,Z,P,X,ys = single_data_from_sql(row_time_info)
                plot_overlay(axs[0],R,Z,P,color,f"S:{shot},T:{time}")
                # 绘制参数图
                plot_param(axs[1:],X,ys,color)

    # 固定参数图的高度
    param_y_limit(axs[1:])
    # 保存到内存里
    file = BytesIO()
    fig.savefig(file,format="png",bbox_inches = 'tight')
    # 从内存中读出图像数据转为json字符串
    file.seek(0)
    dic = base64.b64encode(file.read())
    data_json_str = json.dumps(dic,cls=MyEncoder).strip("\"")

    return is_ok,data_json_str


# 绘制动画
@jwt_required()
def gif() -> str:
    is_ok = True
    err_msg = ""

    # 加载数据
    data = request.get_data()
    json_data = json.loads(data)

    dic = {}
    shot = json_data["shot"]
    if os.path.exists(f"{STATIC_PATH}/{shot}.gif"):
        dic = {"url" : f"http://127.0.0.1:5000/static/{shot}.gif"}
        
    return is_ok,dic



# 绘制波形图
@jwt_required()
def waveform() -> str:
    is_ok = True
    err_msg = ""

    # 加载数据
    json_data = request.get_json()
    
    is_follow = json_data.get("is_follow",0)
    params = json_data.get("params",["p1","p2","p3","p4","p5","p6","p7","p8","p9"])
    shot_list = json_data.get("shot_list")

    datas = []
    for shot in shot_list:
        dic = {shot:[]}
        shot_info =  ShotInfo.query.filter(ShotInfo.shot==shot,ShotInfo.is_follow==is_follow).first()
        if shot_info:
            rows_time_info = TimeInfo.query.filter(TimeInfo.shot_info_id==shot_info.id).all()
            for row_time_info in rows_time_info:
                dic[shot].append(row_time_info.time)
        datas.append(dic)

    full_params = ["p1","p2","p3","p4","p5","p6","p7","p8","p9"]
    
    

    fig,axs = get_wave_fig(params,12)
    for i,data in enumerate(datas):
        
        full_params_idc = {}
        for param in full_params:
            full_params_idc[param] = []
        color = COLOR_LIST[i%len(COLOR_LIST)]

        for k,v in data.items():

            shot = k
            times = v

            shot_info = ShotInfo.query.filter(ShotInfo.shot==shot,ShotInfo.is_follow==is_follow).first()
            if shot_info:
                rows_time_info = TimeInfo.query.filter(TimeInfo.shot_info_id==shot_info.id,TimeInfo.time.in_(times)).all()
                for row_time_info in rows_time_info:
                    full_params_idc["p1"].append(row_time_info.p1)
                    full_params_idc["p2"].append(row_time_info.p2)
                    full_params_idc["p3"].append(row_time_info.p3)
                    full_params_idc["p4"].append(row_time_info.p4)
                    full_params_idc["p5"].append(row_time_info.p5)
                    full_params_idc["p6"].append(row_time_info.p6)
                    full_params_idc["p7"].append(row_time_info.p7)
                    full_params_idc["p8"].append(row_time_info.p8)
                    full_params_idc["p9"].append(row_time_info.p9)
                

            plot_waveform(axs,times,params,full_params_idc,shot,color)

    # 对齐ylabel
    # fig.align_ylabels()
    # 保存到内存里
    file = BytesIO()
    fig.savefig(file,format="png",bbox_inches = 'tight')
    # 从内存中读出图像数据转为json字符串
    file.seek(0)
    dic = base64.b64encode(file.read())
    data_json_str = json.dumps(dic,cls=MyEncoder).strip("\"")


    return is_ok,data_json_str



if __name__ == "__main__":
    ...
