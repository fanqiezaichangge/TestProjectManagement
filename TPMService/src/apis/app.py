from flask import Blueprint
from flask import request
import pymysql
from dbutils.pooled_db import PooledDB
from ..configs import configs

app_application = Blueprint("app_application", __name__)

pool = PooledDB(pymysql, 3,
                host=configs.MYSQL_HOST,
                port=configs.MYSQL_PORT,
                user=configs.MYSQL_USER,
                passwd=configs.MYSQL_PASSWORD,
                database=configs.MYSQL_DATABASE)


@app_application.route("/api/app/list", methods=["POST"])
def application_list():
    body = request.get_json()
    print(body)
    response = {
        'code': 20000,
        'message': 'OK',
        'data': []
    }

    sql = ''

    if body.get('appId'):
        sql += " AND a.`appID` like '%{}%'".format(body['appID'])
    if body.get('productId'):
        sql += " AND a.`productId` like '%{}%'".format(body['productId'])
    if body.get('note'):
        sql += " AND a.`note` like '%{}%'".format(body['note'])
    if body.get('developer'):
        sql += " AND a.`developer` like '%{}%'".format(body['developer'])
    if body.get('producer'):
        sql += " AND a.`producer` like '%{}%'".format(body['producer'])
    if body.get('tester'):
        sql += " AND a.`tester` like '%{}%'".format(body['tester'])

    page = body['page']
    size = body['size']
    offset = (page - 1) * size
    sql_res = 'SELECT a.`appId`,a.`note`,p.`title`,a.`developer`,a.`producer`,a.`tester`,a.`updateDate` FROM `apps` a left join `products` p on a.`productId` = p.`id` WHERE a.`status`=0' \
              + sql \
              + ' ORDER BY `updateDate` DESC LIMIT {},{}'.format(offset, size)
    count_sql = 'SELECT count(*) from `apps` a WHERE `status`=0' + sql

    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            print(sql_res)
            print(count_sql)
            cursor.execute(sql_res)
            data = cursor.fetchall()
            cursor.execute(count_sql)
            count = cursor.fetchone()
            count = count['count(*)']
            print(count)

            response = {
                'code': 20000,
                'data': data,
                'message': 'OK',
                'page': body['page'],
                'pages': count//size + 1,
                'total': count,
            }
            return response


@app_application.route("/api/app/add", methods=["POST"])
def application_add():
    response = {
        'code': 20000,
        'message': 'ok'
    }
    body = request.get_json()
    if not body['appId']:
        response = {
            'code': 50000,
            'message': '应用ID必填'
        }
        return response
    if not body['productId']:
        response = {
            'code': 50000,
            'message': '归属产品必填'
        }
        return response
    if not body['note']:
        response = {
            'code': 50000,
            'message': 'APP名称必填'
        }
        return response
    if not body['developer']:
        response = {
            'code': 50000,
            'message': 'developer必填'
        }
        return response
    if not body['producer']:
        response = {
            'code': 50000,
            'message': 'producer必填'
        }
        return response
    if not body['tester']:
        response = {
            'code': 50000,
            'message': 'tester必填'
        }
        return response
    if not body['createUser']:
        response = {
            'code': 50000,
            'message': 'createUser必填'
        }
        return response
    if not body['operator']:
        response = {
            'code': 50000,
            'message': 'operator必填'
        }
        return response
    # body['appId']
    # body['productId']
    # 'note'
    # 'tester'
    # 'developer'
    # 'producer'
    # 'CcEmail'
    # 'gitCode'
    # 'wiki'
    # 'more'
    # 'creteUser'
    # 'createDate'
    # 'updateUser'
    # 'updateDate'

    with pool.connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `apps` (`appID`,`productId`,`status`,`note`,`tester`,`developer`,`producer`,`creteUser`,`createDate`,`updateUser`,`updateDate`) " \
                  "VALUES ('{0}',{1},'0','{2}','{3}','{4}','{5}','{6}',NOW(),'{7}',NOW())"\
                .format(body['appId'], body['productId'], body['note'], body['tester'], body['developer'], body['producer'], body['createUser'], body['operator'])
            print(sql)
            cursor.execute(sql)
            connection.commit()
            return response

