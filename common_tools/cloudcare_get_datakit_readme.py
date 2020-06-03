# -*- coding: utf-8 -*-
"""
==========================================================================================
创建于2020-06-01（by jingxue.huang）: 自动根据配置文件，指标梳理文件生成readme
==========================================================================================
"""
# Build-in Modules
import json

# 3rd-part Modules
import argparse
from jinja2 import Template
import excelrd

class Readexcel:
    """
    参数：
    文件名，sheet名，列数，行数
    输出相应结果
    """
    def __init__(self):
        pass

    def table_head(self, **kwargs):
        book = excelrd.open_workbook(kwargs['excelfile'])
        sh = book.sheet_by_name(kwargs['excelsheet'])

        if kwargs['excelrows'] == 'all':
            kwargs['excelrows'] = sh.nrows

        if kwargs['excelcols'] == 'all':
            kwargs['excelcols'] = sh.ncols

        datas = []
        table_head_1 = ['----']
        for row_idx in range(1):
            for col_idx in range(kwargs['excelcols']):
                cell = sh.cell(row_idx, col_idx)
                if not cell.value:
                    continue
                data = ("{}".format(cell.value))
                datas.append(data)
        num = kwargs['excelcols']
        table_heads_1 = table_head_1 * num
        return datas,table_heads_1

    def table_body(self, **kwargs):
        book = excelrd.open_workbook(kwargs['excelfile'])
        sh = book.sheet_by_name(kwargs['excelsheet'])

        if kwargs['excelrows'] == 'all':
            kwargs['excelrows'] = sh.nrows

        if kwargs['excelcols'] == 'all':
            kwargs['excelcols'] = sh.ncols

        datas = []
        for row_idx in range(1,kwargs['excelrows']):
            data = sh.row_values(row_idx,0,kwargs['excelcols'])
            datas.append(data)
        return datas

class Readconf:
    def __init__(self):
        pass


    def startup(self,**kwargs):
        datas = ''
        with open(kwargs['confile'], encoding='utf-8') as lines:
            for line in lines:
                datas = '%s%s' % (datas, line)
            return datas

class GetReadme:
    """
    渲染视图模板Readme到前端
    """

    def __init__(self, **kwargs):
        self.render_data = kwargs

    def render_template(self):
        template_data = """{% for _data in data %}# {{_data.engine}}监控指标采集
## 简介
采集 {{_data.engine}} 监控指标上报到DataFlux中

## 前置条件
- 已安装Datakit [DataKit 安装文档](https://help.dataflux.cn/doc/0c6ebce225784bd2ad994d5f89c5dbc89e025792)

## 配置
{{_data.engine}}数据库授权监控账号
```sql
```

打开 DataKit 采集源配置文件夹（默认路径为 DataKit 安装目录的 conf.d 文件夹），找到 {{_data.datakitdir}}文件夹，打开里面的 {{_data.datakitdir}}.conf。
```shell
{{_data.confile}}
```

配置好后，重启 DataKit 即可生效。
```shell
systemctl restart datakit
```

## 采集指标
{{_data.fields}}

## 标签
待补充
{% endfor %}
        """
        template = Template(template_data)
        return template.render(**self.render_data)

    def maker(self, out_dir):
        file_name = 'index.md'
        result = self.render_template()
        with open('{}/{}'.format(out_dir, file_name), 'w', encoding='utf8') as f:
            f.write(result)

def starup(**kwargs):

    # 1.根据conf文件内容生成变量值
    confs = Readconf()
    conf = confs.startup(**params)

    # 2.根据excel文件内容生成变量值
    new_list = []
    excels = Readexcel()
    table_head = excels.table_head(**params)
    for _table_head in table_head:
        new_list.append(_table_head)

    table_body = excels.table_body(**params)
    for _table_body in table_body:
        new_list.append(_table_body)

    fields = ''
    for list in new_list:
        fields = '%s%s%s' % (fields, '|'.join(list), '\n')

    # 3.渲染报告
    # temp_data = {'data':[{},{},{}]}


    data = [{'engine': kwargs['engine'],
             'datakitdir': kwargs['datakitdir'],
             'fields' : fields,
             'outdir': kwargs['outdir'],
             'confile': conf
             }]

    temp_data = {
        'data': data,
    }

    # print(temp_data)

    report = GetReadme(**temp_data)
    report.maker(kwargs['outdir'])


if __name__ == "__main__":
    """
    必要参数：
    数据库类型标准名，
    数据库类型别名，
    输出目录名,
    输入excel文件名    
    """
    parser = argparse.ArgumentParser(description='''数据库视图模板Readme
    Example：
        python3 get_jinjia2_test.py --Engine ENGINE --DatakitDir DATAKITDIR --ExcelFile EXCELFILE --OutDir OUTDIR --ConfFile CONFFILE
        python3 get_jinjia2_test.py  get_jinjia2_test.py --Engine MongoDB --DatakitDir mongodb --ExcelFile namesdemo1.xlsx --ExcelSheet oracle_monitor的tag  --ExcelRows 7 --ExcelCols 4 --OutDir ./report --ConfFile ./mongo.conf
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--Engine", help='''Engine 必要参数 只能选择一种类型''')
    parser.add_argument("--DatakitDir", help="DatakitDir 必要参数")
    parser.add_argument("--ExcelFile", help="ExcelFile 必要参数")
    parser.add_argument("--ExcelSheet", help="ExcelSheet 必要参数")
    parser.add_argument("--ExcelRows", default='all',help="ExcelRows 非必要参数，不指定默认all，也可指定例如 2")
    parser.add_argument("--ExcelCols", default='all',help='''ExcelCols 非必要参数，不指定默认all，也可指定例如 2''')
    parser.add_argument("--OutDir", help="输出目录 必要参数 需要提前创建该目录")
    parser.add_argument("--ConfFile", help="配置文件")


    args = parser.parse_args()

    params = {
        'engine': args.Engine,
        'datakitdir' : args.DatakitDir,
        'excelfile' : args.ExcelFile,
        'excelsheet' : args.ExcelSheet,
        'excelrows' : args.ExcelRows,
        'excelcols' : args.ExcelCols,
        'outdir': args.OutDir,
        'confile' : args.ConfFile
    }

    if args.ExcelRows.isdigit():
        params['excelrows'] = int(args.ExcelRows)

    if args.ExcelCols.isdigit():
        params['excelcols'] = int(args.ExcelCols)

    # 此处需要完善：异常抛出
    starup(**params)



