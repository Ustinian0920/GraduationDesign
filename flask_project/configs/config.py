"""
普通配置,如三方 url， 数据库等
"""
import os

# 数据库连接字符串
SQLALCHEMY_DATABASE_URI =   "mysql+pymysql://root:repeatlink@localhost:3306/test"

# 数据库自动提交
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# 数据库追踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = True

# JWT的加密秘钥
JWT_SECRET_KEY = 'super-secret'

# JWT允许token黑名单
JWT_BLACKLIST_ENABLED = True

# JWT检查access token
JWT_BLACKLIST_TOKEN_CHECKS = 'access'


BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))  # 项目目录

PROJECT_NAME = BASEDIR.split(os.path.sep)[-1]  # 项目名称
ENV = os.environ.get(f'{PROJECT_NAME}_ENV', 'LOCAL')  # PROD/UAT/DEV/LOCAL
DBTYPE = "mysql"  # mongo/arangodb/dm/mysql etc


