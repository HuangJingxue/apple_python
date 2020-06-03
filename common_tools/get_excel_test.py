# -*- coding: utf-8 -*-
"""
==========================================================================================
创建于2020-06-01（by jingxue.huang）: 测试excel内容读取
==========================================================================================
"""
# Build-in Modules
import json

# 3rd-part Modules
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
        book = excelrd.open_workbook(kwargs['filename'])
        sh = book.sheet_by_name(kwargs['sheetname'])

        if kwargs['rows'] == all:
            kwargs['rows'] = sh.nrows

        if kwargs['cols'] == all:
            kwargs['cols'] = sh.ncols

        datas = []
        table_head_1 = ['----']
        for row_idx in range(1):
            for col_idx in range(kwargs['cols']):
                cell = sh.cell(row_idx, col_idx)
                if not cell.value:
                    continue
                data = ("{}".format(cell.value))
                datas.append(data)
        num = kwargs['cols']
        table_heads_1 = table_head_1 * num
        return datas,table_heads_1

    def table_body(self, **kwargs):
        book = excelrd.open_workbook(kwargs['filename'])
        sh = book.sheet_by_name(kwargs['sheetname'])

        if kwargs['rows'] == all:
            kwargs['rows'] = sh.nrows

        if kwargs['cols'] == all:
            kwargs['cols'] = sh.ncols

        datas = []
        for row_idx in range(1,kwargs['rows']):
            data = sh.row_values(row_idx,0,kwargs['cols'])
            datas.append(data)
        return datas

if __name__=="__main__":
    '''
    所有行数 'rows' : all
    所有列数 'cols' : all
    '''
    params = {
        'filename': "namesdemo1.xlsx",
        'sheetname': "oracle_monitor的tag",
        'rows': all,
        'cols': all,
    }
    new_list = []
    t = Readexcel()
    table_head = t.table_head(**params)
    for _table_head in table_head:
        new_list.append(_table_head)


    table_body = t.table_body(**params)
    for _table_body in table_body:
        new_list.append(_table_body)

    # print(new_list)
    b = ''
    for list in new_list:
        b = '%s%s%s' % (b, '|'.join(list), '\n')

    print(b)








