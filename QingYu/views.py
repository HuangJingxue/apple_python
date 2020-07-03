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

#理财渠道
class MyV_RE(MyModelView):
    column_labels = {
        'id': u'编号',
        'channelname': u'渠道名称',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'channelname', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'channelname', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'channelname': [
            ('支付宝', '支付宝'),
            ('招行app', '招行app'),
            ('小她理财', '小她理财'),
            ('蛋卷理财', '蛋卷理财')
        ]
    }
#健身
class MyV_BB(MyModelView):
    column_labels = {
        'id': u'编号',
        'channelname': u'渠道名称',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'channelname', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'channelname', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'channelname': [
            ('支付宝', '支付宝'),
            ('招行app', '招行app'),
            ('小她理财', '小她理财'),
            ('蛋卷理财', '蛋卷理财')
        ]
    }

#理财渠道
class MyV_FC(MyModelView):
    column_labels = {
        'id': u'编号',
        'channelname': u'渠道名称',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'channelname', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'channelname', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'channelname': [
            ('支付宝', '支付宝'),
            ('招行app', '招行app'),
            ('小她理财', '小她理财'),
            ('蛋卷理财', '蛋卷理财'),
        ]
    }

#理财类型
class MyV_FT(MyModelView):
    column_labels = {
        'id': u'编号',
        'typename': u'类型名称',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'typename', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'typename', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'typename': [
            ('货币基金', '货币基金'),
            ('债券基金', '债券基金'),
            ('混合基金', '混合基金'),
            ('股票基金', '股票基金'),
            ('银行理财', '银行理财'),
            ('打新债', '打新债'),
            ('国债逆回购', '国债逆回购'),
            ('兼职','兼职'),
        ]
    }

#理财明细
class MyV_FI(MyModelView):
    column_labels = {
        'id': u'编号',
        'fchannel.id': u'渠道ID',
        'ftype.id': u'类型ID',
        'fundname': u'基金名称',
        'amount': u'金额',
        'status': u'状态',
        'info': u'备注',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'channelid','typeid','fundname', 'amount', 'status', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'channelid','typeid', 'fundname', 'amount', 'status', 'info', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'status': [
            ('新购', '新购'),
            ('追加', '追加'),
            ('卖出', '卖出')
        ]
    }