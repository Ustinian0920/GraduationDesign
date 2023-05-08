"""app间通用的model优化至此处"""
from apps.common_errorcode import CODE_REFS_CN as CODE_REFS
from flask_restful import Resource

class V1Response(object):
    def __init__(self):
        self.results = {}
        self.results['return_code'] = "OK"
        self.results['return_msg'] = CODE_REFS['OK']
        self.results['data'] = {}

    def is_ok(self):
        if self.results['return_code'] == "OK":
            return True
        else:
            return False

    def set_data(self, key, value):
        if key == 'data':
            self.results[key] = value
        else:
            self.results['data'][key] = value

    def set_error(self, err_code, err_detailmsg = ""):
        if err_code in CODE_REFS:
            self.results['return_msg'] = CODE_REFS[err_code] + err_detailmsg
        else:
            self.results['return_msg'] = CODE_REFS['ERR_UNKOWN']
        self.results['return_code'] = err_code
        
    def get_response(self):
        return self.results

class XQResource(Resource):
    def __init__(self):
        self.rep = V1Response()