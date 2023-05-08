"""app之间有些通用的逻辑放到此文件中,被各app中的control引用"""
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import imageio.v2 as imageio
import json
import os
from flask_jwt_extended import get_current_user
from apps.user.model import User

STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),"static")
COLOR_LIST = ["#fed631","#3dfffe","#fed631"]
def time_to_str(date_time):
    if date_time == None:
        return None
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


# json解析
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        判断是否为bytes类型的数据是的话转换成str
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

def single_data_from_sql(row):
    R = np.fromstring(row.R,dtype=np.float64).reshape(25,25)
    Z = np.fromstring(row.Z,dtype=np.float64).reshape(25,25)
    P = np.fromstring(row.P,dtype=np.float64).reshape(25,25)
    X = np.fromstring(row.X,dtype=np.float64)
    y1 = np.fromstring(row.y1,dtype=np.float64)
    y2 = np.fromstring(row.y2,dtype=np.float64)
    y3 = np.fromstring(row.y3,dtype=np.float64)
    y4 = np.fromstring(row.y4,dtype=np.float64)
    y5 = np.fromstring(row.y5,dtype=np.float64)

    return R,Z,P,X,[y1,y2,y3,y4,y5]

def plot_background():
    fig = plt.figure(figsize=(10.4,6.08),dpi=100)
    plt.subplots_adjust(top = 0.98, bottom = 0, right = 1, left = 0, hspace=0.5,wspace=0.28)
    plt.margins(0,0)
    ax1 = plt.subplot2grid((58,128),(0,10),rowspan=53,colspan=38)
    ax2 = plt.subplot2grid((58,128),(4,70),rowspan=9,colspan=49)
    ax3 = plt.subplot2grid((58,128),(14,70),rowspan=9,colspan=49)
    ax4 = plt.subplot2grid((58,128),(24,70),rowspan=9,colspan=49)
    ax5 = plt.subplot2grid((58,128),(34,70),rowspan=9,colspan=49)
    ax6 = plt.subplot2grid((58,128),(44,70),rowspan=9,colspan=49)
    axs = [ax1,ax2,ax3,ax4,ax5,ax6]
    for ax in axs[1:-1]:
        ax.set_xticklabels(["1"],color="white")
    ax1.set_title("psi")
    ax1.set_ylabel("Z(m)")
    ax1.set_xlabel("R(m)")
    ax6.set_xlabel("Time(ms)")
    ax2.set_ylabel("li")
    ax3.set_ylabel("q")
    ax4.set_ylabel("mhd")
    ax5.set_ylabel("V")
    ax6.set_ylabel("rhom")
    return fig,axs

def plot_contour(ax1,R,Z,P):
    ax1.contour(R,Z,P,np.linspace(0,0.05,5),colors="red")
    ax1.contour(R,Z,P,np.linspace(0.5,4,6),colors="#fed631")
    ax1.contour(R,Z,P,np.linspace(4,6,7),colors="#3dfffe")
    ax1.contour(R,Z,P,[4],colors="red")
    ax1.contour(R,Z,P,np.linspace(6,52,20),colors="#fed631")

    


def plot_overlay(ax1,R,Z,P,color,label):
    ax1.contour(R,Z,P,np.linspace(0,4,8),colors=color)
    ax1.plot([0,0],[0,0],color=color,label=label)
    ax1.legend(loc=4,fontsize=6)

def get_wave_fig(params,width):
    # 根据 绘图数量 计算尺寸
    if (len(params)%2)==1:
        row=len(params)//2+1
        num=1
    else:
        row=len(params)//2
        num=0          
    fig,axs=plt.subplots(row,2,figsize=(width,row*width*0.14))
    fig.subplots_adjust(hspace=0.7,wspace=0.4)

    # 移除多余的子图
    if num:
        if row==1:
            axs[1].remove()
        else:
            axs[row-1,1].remove()

    return fig,axs


def plot_waveform(axs,times,params,full_params_dic,shot,color):
    for i,param in enumerate(params):
        label = f"shot:{shot}"
        
        axs[i//2,i%2].plot(times,full_params_dic.get(param,times),color=color,label=label)
        axs[i//2,i%2].legend(loc=4,fontsize=6)
        axs[i//2,i%2].set_ylabel(param)
        axs[i//2,i%2].set_xlabel("Time")
    



def plot_param(axs,X,ys,color):
    print(f"len_axs:{len(axs)}")
    print(f"len_ys:{len(ys)}")
    for i,ax in enumerate(axs):
        ax.plot(X,ys[i],color=color)

def param_y_limit(axs):
    for ax in axs:
        ax.set_ylim(2.9,8.1)    

def plot_gif_frame(shot,time,R,Z,P,X,ys,color):

    fig,axs = plot_background()
    
    

    buf = BytesIO()
    plot_contour(axs[0],R,Z,P)
    plot_param(axs[1:],X,ys,color)
    param_y_limit(axs[1:])
    axs[1].set_title(f"Shot:{shot} Time:{time}")
    plt.savefig(buf,bbox_inches = 'tight')
    frame = imageio.imread(buf)
    buf.close()

    return frame

def get_current_user_info():
    user_name = get_current_user()
    print(user_name)
    user = User.query.filter(User.name==user_name).first()
    dic = {}
    if user:
        dic = {"id":user.id,"is_manager":True if user.manager==1 else False}
       
    return dic

if __name__=="__main__":
    print(get_current_user())

