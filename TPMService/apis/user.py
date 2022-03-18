from flask import Blueprint
import json
from flask import request

app_user = Blueprint("app_user", __name__)


@app_user.route("/api/user/login", methods=['POST'])
def login():
    # js_data = request.get_json()
    data = request.get_data()
    js_data = json.loads(data)

    if 'username' in js_data and js_data['username'] == 'admin':
        result_success = {"code":20000,"data":{"token":"admin-token"}}
        return result_success
    else:
        result_error = {"code":60204,"message":"账号密码错误"}
        return result_error


@app_user.route("/api/user/info", methods=['GET'])
def info():
    token = request.args.get("token")
    if token == 'admin-token':
        result_success = {
            "code": 20000,
            "data": {
                "role": ["admin"],
                "introduction": "I am a super administrator",
                "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
                "name": "Super Admin"
            }
        }
        return result_success
    else:
        result_error = {
            "code": 60204,
            "message": "用户信息不正确"
        }
        return result_error



