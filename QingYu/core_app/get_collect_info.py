# -*- coding: utf-8 -*-

# Build-in Modules
import json
import datetime
import decimal
import os
import json
import time
#import locale
import io
import zipfile
import shutil
# 3rd-part Modules
import argparse
import pymysql
import xlsxwriter
#import sys
from jinja2 import Template

#defaultencoding = 'utf-8'
#if sys.getdefaultencoding() != defaultencoding:
#    reload(sys)
#    sys.setdefaultencoding(defaultencoding)
now_date = time.strftime('%Y%m%d', time.localtime())

class OSHelper:
    def __init__(self):
        pass

    def mkdir(self, path):
        """
        在当前目录下创建子目录
        """
        try:
            os.makedirs(path)
        except Exception as e:
            print(str(e))
            return path
        else:
            return path

    def rmdir(self, path):
        """
        递归删除目录
        """
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(str(e))
            return path
        else:
            return path

    def rmfile(self, path):
        """
        删除文件
        """
        try:
            os.remove(path)
        except Exception as e:
            print(str(e))
            return path
        else:
            return path


def make_zip(source_dir, output_filename):
    # 打包目录为zip文件（未压缩）
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    return output_filename

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

# 3.2 渲染到markdown
class GetReadme:
    """
    渲染视图模板Readme到前端
    """

    def __init__(self, **kwargs):
        self.render_data = kwargs

    def render_template(self):
        template_data = """{% for _data in data %}# {{_data.collector}}采集器说明
## 简介
采集 {{_data.collector}} 监控指标上报到DataFlux中

## 前置条件
- 已安装Datakit [DataKit 安装文档](https://help.dataflux.cn/doc/0c6ebce225784bd2ad994d5f89c5dbc89e025792)

## 配置
{{_data.collector}}数据库授权监控账号
```sql
```

配置好后，重启 DataKit 即可生效。
```shell
systemctl restart datakit
```

## 采集指标
{{_data.fields}}

{% endfor %}
        """
        template = Template(template_data)
        return template.render(**self.render_data)

    def maker(self, out_dir, collector):
        file_name = '{}.md'.format(collector)
        result = self.render_template()
        with io.open('{}/{}'.format(out_dir, file_name), 'w', encoding='utf-8') as f:
            f.write(result)


# 4.将SQL内容输入到sheet当中输出
def startup(**kwargs):
    out_type = kwargs['out_type']
    params = {
        'url': kwargs['url'],
        'port': kwargs['port'],
        'username': kwargs['username'],
        'password': kwargs['password'],
        'dbname': kwargs['dbname'],
        'collector': kwargs['collectors'],
    }
    # 删除历史输出文件
    os_api = OSHelper()
    directory = os.getcwd()
    dir_name = 'out_put'
    zip_name = '.'.join([dir_name, 'zip'])
    path = os.path.join(directory, dir_name)
    path_zip = os.path.join(directory, zip_name)
    os_api.rmdir(path)
    os_api.rmfile(path_zip)
    dir_name = os_api.mkdir(dir_name)
    # print(dir_name)
    for collector in kwargs['collectors']:
        params_excel = {
            'collector': collector,
            'dir_name': dir_name,
        }
        # 1.根据传递的参数对报告后端逻辑进行过滤
        info_api = MysqlInfo(collector)
        sql_list = info_api.get_info()
        # print(json.dumps(sql_list, indent=2, ensure_ascii=False))

        # 2.获取待渲染的报告数据
        mysql_api = MysqlHelper(**params)

        if out_type == 'excel':
            excel_api = Outputexcel(**params_excel)
            for sql in sql_list:
                # print(sql["query"])
                sql_result = mysql_api.col_query(sql["query"])
                # 3.渲染报告
                excel_api.add_sheet(sql["desc"], sql["fields"], sql["list_keys"], sql_result)
            excel_api.write_close()
        elif out_type == 'markdown':
            new_filed = ''
            for sql in sql_list:
                head = sql['fields']
                num = len(head)
                head_line = ['----']
                head_lines = head_line * num
                new_filed = '{}{}\n{}\n{}'.format(new_filed, sql['desc'], '|'.join(head), '|'.join(head_lines))
                sql_result = mysql_api.col_query(sql["query"])
                for sqlr in sql_result:
                    new_filed = '{}\n{}'.format(new_filed, '|'.join(
                        list(map(lambda x: x if isinstance(x, str) else '',sqlr))
                    ))
                new_filed = '{}\n'.format(new_filed)
            data = [{'collector': collector,
                     'fields': new_filed
                     }]

            temp_data = {
                'data': data,
            }

            # print(temp_data)

            report = GetReadme(**temp_data)
            report.maker(path, collector)

    # 打包
    zip_file = make_zip(dir_name, '.'.join([dir_name, 'zip']))
    return zip_file

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
