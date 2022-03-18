from flask import Blueprint
from flask import request
import pymysql.cursors

app_product = Blueprint("app_product", __name__)


def connectDB():
    connection = pymysql.connect(host='localhost',   # 数据库IP地址或链接域名
                             user='root',     # 设置的具有增改查权限的用户
                             password='123456', # 用户对应的密码
                             database='tpmdatas',# 数据表
                             charset='utf8mb4',  # 字符编码
                             cursorclass=pymysql.cursors.DictCursor) # 结果作为字典返回游标
    # 返回新的书库链接对象
    return connection


connection = connectDB()


@app_product.route("/api/product/list", methods=["GET"])
def product_list():
    with connection.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT * FROM `Products` ORDER BY `Update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    # data = [
    #     {"id": 1, "keyCode": "project1", "title": "项目一", "desc": "这是项目1描述", "operator": "admin",
    #      "update": "2020-04-06"},
    #     {"id": 2, "keyCode": "project2", "title": "项目而", "desc": "这是项目2描述", "operator": "user", "update": "2020-04-03"}
    # ]

    result_success = {
        "code": 20000,
        "data": data
    }
    return result_success


@app_product.route("/api/product/add", methods=["POST"])
def add_product():
    response_success = {
        "code": 20000,
        "message": "add success",
        "data": []
    }

    body = request.get_json()

    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s"
            cursor.execute(select, (body["keyCode"],))
            result = cursor.fetchall()

    if len(result) > 0:
        response_success["code"] = 20001
        response_success["message"] = "号码有重复"
        return response_success

    with connection.cursor() as cursor:
        sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"]))
        connection.commit()

    return response_success
