
from apps.draw.errorcode import CODE_REFS_CN as draw_errcode
from apps.edit.errorcode import CODE_REFS_CN as edit_errcode
from apps.home.errorcode import CODE_REFS_CN as home_errcode
from apps.user.errorcode import CODE_REFS_CN as user_errcode

CODE_REFS_CN = {
    "OK": "操作成功。",
    "ERR_UNKOWN": "未知的错误类型",
    "ERR_SYS_DB_ERROR": "数据库错误。",
    "ERR_INAVLID_LOGIN": "错误的用户名或者密码。",
    "ERR_USER_ALREADY_EXIST": "用户已经存在，请尝试别的用户名。",
    "ERR_LOGOUT": "用户登出错误。",
    "ERR_UNABLE_UPDATE_RELEASE_INFO": "更新版本信息错误。",
    "ERR_UNABLE_FIND_CLIENT": "找不到指定的客户。",
    "ERR_PARAMETER": "参数错误",
    "ERR_TOKEN_ERR":"token无效",
    "ERR_TOKEN_EXPIRED":"token过期了",
    "ERR_FILE_NAME":"文件名错误",
    "ERR_FILE_EXISTS":"文件已经存在",
}


CODE_REFS_CN.update(draw_errcode)
CODE_REFS_CN.update(edit_errcode)
CODE_REFS_CN.update(home_errcode)
CODE_REFS_CN.update(user_errcode)
