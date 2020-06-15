# -*- coding: utf-8 -*-

# Build-in Modules
import json
import datetime
import decimal
import os
import json
import time
import locale
# 3rd-part Modules
import argparse
import pymysql
import xlsxwriter
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
now_date = time.strftime('%Y%m%d', time.localtime())

# 1.连接MySQL数据库
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


# 2.获取指标类型、指标明细、全局标签SQL定义好
class MysqlInfo:
    """
    获取报告需要的后端逻辑
    """

    def __init__(self, collector):
        """
        数据库后端逻辑
        """

        metric_type = """select business,requires,requestor,requires_sql from business_require where business = '{0}'""".format(collector)

        self.sql_params = [
            {
                'query': metric_type,
                'desc': "业务需求",
                'fields': ["业务", "需求", "提交人", "需求SQL"],
		'list_keys': ["business","requires",'requestor','requires_sql']
            }
        ]

    def get_info(self):
        """
        返回SQL
        """
        return self.sql_params


# 3.定义excel中输入的字段名和sheet名
class Outputexcel():
    def __init__(self, **kwargs):
        self.file_name = '{}业务需求明细{}.xlsx'.format(kwargs['collector'], now_date)
        self.workbook = xlsxwriter.Workbook(self.file_name)

    def write_file_column(self, work, worksheet, list_name):
        top = self.workbook.add_format(
            {'border': 1, 'align': 'center', 'bg_color': '#FF9966', 'font_size': 10, 'bold': True})  # 设置单元格格式
        j = 0
        for i in list_name:
            worksheet.write(0, j, i, top)
            j += 1

    def add_sheet(self, sheet_name, fields, list_keys, lines):
        column = self.workbook.add_format({'border': 1, 'align': 'center', 'font_size': 10})
        worksheet = self.workbook.add_worksheet(sheet_name)

        for _c in range(len(list_keys)):
            worksheet.set_column('{0}:{0}'.format(chr(_c + ord('A'))), 30)
        self.write_file_column(self, worksheet, fields)
        row = 1
        for data in lines:
            # print(data)
            for col, filed in enumerate(data):
                # print(col,filed)
                worksheet.write(row, col, filed)
            row += 1

    def write_close(self):
        self.workbook.close()


# 4.将SQL内容输入到sheet当中输出
def startup(**kwargs):
    params = {
        'url': kwargs['url'],
        'port': kwargs['port'],
        'username': kwargs['username'],
        'password': kwargs['password'],
        'dbname': kwargs['dbname'],
        'collector': kwargs['collector'],
    }
    # 1.根据传递的参数对报告后端逻辑进行过滤
    info_api = MysqlInfo(params['collector'])
    sql_list = info_api.get_info()
    # print(json.dumps(sql_list, indent=2, ensure_ascii=False))

    # 2.获取待渲染的报告数据
    mysql_api = MysqlHelper(**params)
    excel_api = Outputexcel(**params)
    for sql in sql_list:
        # print(sql["query"])
        sql_result = mysql_api.col_query(sql["query"])
        # 3.渲染报告
        excel_api.add_sheet(sql["desc"], sql["fields"], sql["list_keys"], sql_result)
    excel_api.write_close()
    return excel_api.file_name


if __name__ == "__main__":
    # 测试
    params = {
        'collector': 'mes',
        'url': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'root123',
        'dbname': 'myweb',
    }
    file_name = startup(**params)
    print(file_name)
