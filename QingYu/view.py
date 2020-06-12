# -*- coding:utf8 -*-
from flask_admin.contrib.sqla import ModelView
import flask_login as login


# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    # 展示表详情
    can_view_details = True
    # can_delete = False
    # 导出功能
    can_export = True
    export_types = ['csv']
    # 不显示的列
    column_exclude_list = ['uuid', 'is_deleted', 'delete_time']
    # 不创建也不编辑的列
    form_excluded_columns = ['uuid', 'create_time', 'update_time', 'is_deleted', 'delete_time']

class MyV_BR(MyModelView):
    column_labels = {
        'id': u'编号',
        'business': u'业务名',
        'requires': u'业务需求',
        'requires_sql': u'业务需求SQL',
        'requestor': u'需求人',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'business', 'requires', 'requires_sql',
                   'requestor', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'business', 'requires', 'requires_sql',
        'requestor', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'requestor': [
            ('青雨', '青雨'),
            ('衾袭', '衾袭'),
            ('静雪', '静雪')
        ],
        'business': [
            ('mes', 'mes'),
            ('cem', 'cem'),
            ('ky', 'ky'),
            ('od', 'od')
        ]
    }
