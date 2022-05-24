from flask import Blueprint
from flask import request
import pymysql
from dbutils.pooled_db import PooledDB
from ..configs import configs

app_product = Blueprint("app_product", __name__)

pool = PooledDB(pymysql, 3,
                host=configs.MYSQL_HOST,
                port=configs.MYSQL_PORT,
                user=configs.MYSQL_USER,
                passwd=configs.MYSQL_PASSWORD,
                database=configs.MYSQL_DATABASE)


# 改成带参数能够模糊查询的
@app_product.route("/api/product/list", methods=["POST"])
def product_list():
    body = request.get_json()
    size = body['size']
    keyCode = body['keyCode']
    title = body['title']
    desc = body['desc']
    offset = body['page'] * size - size
    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 查询产品信息表-按更新时间新旧排序
            sql = "SELECT * FROM `Products` WHERE `status`=0 "
            count = "SELECT count(*) FROM `Products` WHERE `status`=0 "
            if keyCode:
                sql += "AND `keyCode` like '%{}%' ".format(keyCode)
                count += "AND `keyCode` like '%{}%' ".format(keyCode)
            if title:
                sql += "AND `title` like '%{}%' ".format(title)
                count += "AND `title` like '%{}%' ".format(title)
            if desc:
                sql += "AND `desc` like '%{}%' ".format(desc)
                count += "AND `desc` like '%{}%' ".format(desc)
            sql += "ORDER BY `Update` DESC"
            sql += " LIMIT {},{} ".format(offset, size)
            print(sql)
            print(count)
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.execute(count)
            count = cursor.fetchone()
            count = count['count(*)']
            print(count)

        # data = [
        #     {"id": 1, "keyCode": "project1", "title": "项目一", "desc": "这是项目1描述", "operator": "admin",
        #      "update": "2020-04-06"},
        #     {"id": 2, "keyCode": "project2", "title": "项目而", "desc": "这是项目2描述", "operator": "user", "update": "2020-04-03"}
        # ]

        result_success = {
            "code": 20000,
            "data": data,
            "page": body['page'],
            "pages": count//size + 1,
            "total": count
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
    with pool.connection() as connection:
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


@app_product.route("/api/product/update", methods=["POST"])
def update_product():
    resp = {
        'code': 20000,
        'massage': 'OK',
        'data': []
    }
    body = request.get_json()
    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode`=%s"
            cursor.execute(select, (body["keyCode"],))
            result = cursor.fetchall()

            if not result:
                resp['code'] = 20001
                resp['massage'] = '无效的keyCode'
                return resp
            if result and result[0]['id'] != body['id']:
                resp['code'] = 20001
                resp['massage'] = 'keyCode与已有的其他产品重复'

        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            sql = "UPDATE `products` SET `keyCode`=%s, `title`=%s,`desc`=%s,`operator`=%s, `update`= NOW() WHERE id=%s"
            cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"], body['id']))
            connection.commit()

        return resp


@app_product.route("/api/product/delete", methods=["POST"])
def delete_product():
    resp = {
        'code': 20000,
        'message': '删除成功',
        'data': []
    }
    body = request.get_json()
    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            select = "SELECT * FROM `products` WHERE `id`=%s"
            cursor.execute(select, (body['id']),)
            result = cursor.fetchall()

            if not result:
                resp['code'] = 20001
                resp['message'] = '找不到对应ID的产品'
                return resp

        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            sql = "UPDATE `products` SET `status`= 1 WHERE `id` = %s"
            cursor.execute(sql, (body['id'],))
            connection.commit()

        return resp


# 改成带参数能够模糊查询的
@app_product.route("/api/product/listall", methods=["POST"])
def product_listall():
    # body = request.get_json()
    # size = body['size']
    # keyCode = body['keyCode']
    # title = body['title']
    # desc = body['desc']
    # offset = body['page'] * size - size
    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 查询产品信息表-按更新时间新旧排序
            sql = "SELECT * FROM `Products` WHERE `status`=0 "
            print(sql)
            cursor.execute(sql)
            data = cursor.fetchall()
        # data = [
        #     {"id": 1, "keyCode": "project1", "title": "项目一", "desc": "这是项目1描述", "operator": "admin",
        #      "update": "2020-04-06"},
        #     {"id": 2, "keyCode": "project2", "title": "项目而", "desc": "这是项目2描述", "operator": "user", "update": "2020-04-03"}
        # ]

        result_success = {
            "code": 20000,
            "data": data,
        }
        return result_success
