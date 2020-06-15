# -*- coding: utf-8 -*-

# Build-in Modules
import json
import datetime
import decimal
import time

# 3rd-part Modules
import pymysql
import argparse
from jinja2 import Template

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class MysqlHelper:
    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.port = int(kwargs['port'])
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.dbname = kwargs['dbname']
        self.charset = "utf8mb4"
        try:
            self.conn = pymysql.connect(host=self.url, user=self.username, passwd=self.password, port=self.port,
                                        charset=self.charset, db=self.dbname)
            # self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(str(e))
            self.error = 1
        else:
            self.error = 0

    def col_query(self, sql):
        """
        打印表的列名
        :return list
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class GetInfo:
    """
    获取报告需要的后端逻辑
    """

    def __init__(self):
        """
        数据库后端逻辑
        """
        total_ana = '''select count(*) from business_require;'''
        collectors = """select business from business_require where business is not null"""
        self.sql_params = {
            'mysql'.lower(): [
                {
                    'type': 'total_ana',
                    'query': total_ana,
                    'desc': "数据库需求总数",
                    'fields': ["统计"]
                },
                {
                    'type': 'collectors',
                    'query': collectors,
                    'desc': "采集器",
                    'fields': ["采集器"]
                },
            ],
            # 'sqlserver': [{}],
            # 'postgresql': [{}],
            # 'oracle': [{}],
        }

    def get_info(self, engine, filter_infos):
        """
        根据指定的数据库类型 和 报告内容 进行过滤，返回过滤后的SQL
        """
        return list(filter(lambda x: x['type'] in filter_infos, self.sql_params[engine]))


def startup(**kwargs):
    params = {
        'url': kwargs['url'],
        'port': kwargs['port'],
        'username': kwargs['username'],
        'password': kwargs['password'],
        'dbname': kwargs['dbname'],
    }
    # 1.根据传递的参数对报告后端逻辑进行过滤
    info_api = GetInfo()
    sql_list = info_api.get_info(kwargs['engine'], kwargs["info"])
    # print(json.dumps(sql_list, indent=2, ensure_ascii=False))

    # 2.获取待渲染的报告数据
    sql_api = MysqlHelper(**params)
    data = {}
    for sql in sql_list:
        sql_result = sql_api.col_query(sql["query"])
        sql["sql_result"] = sql_result
        data[sql["type"]] = sql
    return data


if __name__ == "__main__":
    # a ='mysql+pymysql://supercloud_dev:Zyadmin@123@10.0.0.29:3306/supercloud_dev?charset=UTF8MB4'
    params = {
        'url': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'root123',
        'dbname': 'myweb',
        'engine': 'mysql',
        'info': [
            'total_ana','collectors'
        ],
    }

    data = startup(**params)
    print(json.dumps(data, cls=CJsonEncoder, ensure_ascii=False, indent=2))
