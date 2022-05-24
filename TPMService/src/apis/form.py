from flask import Blueprint
from flask import request
import pymysql
from dbutils.pooled_db import PooledDB
from ..configs import configs

app_form = Blueprint("app_form", __name__)

pool = PooledDB(pymysql, 3,
                host=configs.MYSQL_HOST,
                port=configs.MYSQL_PORT,
                user=configs.MYSQL_USER,
                passwd=configs.MYSQL_PASSWORD,
                database=configs.MYSQL_DATABASE)


@app_form.route("/api/form/list", methods=["POST"])
def form_list():
    body = request.get_json()
    size = body['size']
    form_id = body.get('form_id')
    form_state = body.get('form_state')
    produce_id = body.get('produce_id')
    current_user = body.get('current_user')
    title = body.get('title')
    created_user_id = body.get('created_user')
    developer_id = body.get('developer')
    tester_id = body.get('tester')
    online_version = body.get('online_version')
    offset = body['page'] * size - size
    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:

            sql = "SELECT * FROM `my_form` WHERE `status`=0 "
            count = "SELECT count(*) FROM `my_form` WHERE `status`=0 "
            if form_id:
                sql += "AND `form_id` like '%{}%' ".format(form_id)
                count += "AND `form_id` like '%{}%' ".format(form_id)
            if title:
                sql += "AND `title` like '%{}%' ".format(title)
                count += "AND `title` like '%{}%' ".format(title)
            if form_state:
                sql += "AND `form_state` = '{}' ".format(form_state)
                count += "AND `form_state` = '{}' ".format(form_state)
            if produce_id:
                sql += "AND `produce_id` = '{}' ".format(form_state)
                count += "AND `produce_id` = '{}' ".format(form_state)
            if current_user:
                sql += "AND `current_user` = '{}' ".format(form_state)
                count += "AND `current_user` = '{}' ".format(form_state)
            if created_user_id:
                sql += "AND `created_user_id` = '{}' ".format(form_state)
                count += "AND `created_user_id` = '{}' ".format(form_state)
            if developer_id:
                sql += "AND `developer_id` = '{}' ".format(form_state)
                count += "AND `developer_id` = '{}' ".format(form_state)
            if tester_id:
                sql += "AND `tester_id` = '{}' ".format(form_state)
                count += "AND `tester_id` = '{}' ".format(form_state)
            if online_version:
                sql += "AND `online_version` = '{}' ".format(form_state)
                count += "AND `online_version` = '{}' ".format(form_state)
            sql += "ORDER BY `modified_time` DESC"
            sql += " LIMIT {},{} ".format(offset, size)
            # print(sql)
            # print(count)
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.execute(count)
            count = cursor.fetchone()
            count = count['count(*)']

            result_success = {
                "code": 20000,
                "data": data,
                "page": body['page'],
                "pages": count // size + 1,
                "total": count
            }
            return result_success


@app_form.route("/api/form/detail", methods=["POST"])
def form_detail():
    body = request.get_json()
    form_id = body['formId']

    with pool.connection() as connection:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM `my_form` WHERE `status`=0 "
            sql += "AND `form_id` = '{}' ".format(form_id)
            cursor.execute(sql)
            data = cursor.fetchone()

            result_success = {
                "code": 20000,
                "data": data,
            }
            return result_success
