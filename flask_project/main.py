from flask import Flask,make_response
# 跨域处理
from flask_cors import CORS
from exts import jwt,db

from werkzeug.utils import import_string
from apps.blueprints import blueprints
import configs.config  as  server_config
from apps.common_model import V1Response

app = Flask(__name__)
app.config.from_object(server_config)
CORS(app, supports_credentials=True) #supports_credentials 允许请求发送cookie
jwt.init_app(app)
db.init_app(app)
db.app = app

# 注册蓝图
for bp_str in blueprints:
    bp = import_string(bp_str)
    app.register_blueprint(bp)


def register_errors(app):
    @app.errorhandler(404)
    def error_404(e):
        return "你所访问的请求不存在，请确认",404,""
    @app.errorhandler(500)
    def error_500(e):
        return "系统错误，请稍后重试",500,""

register_errors(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    res = V1Response()
    res.set_error("ERR_TOKEN_EXPIRED")
    res_data = make_response(res.get_response(),401)
    return res_data

@jwt.user_identity_loader
def _user_identity_lookup(identity):
    return identity


@jwt.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity

@app.route('/health', methods=['GET'])
def health_check():
    """
    检测系统健康
    过程检测数据库及中间件连接
    """
    return "ok"


@app.before_request
def before_request():
    """请求前相关操作，如验证用户token等操作"""
    pass


@app.after_request
def after_request(environ):
    """
    配合前端设置允许跨域等请求后处理操作
    """
    return environ


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)