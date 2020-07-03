# -*- coding:utf8 -*-

from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_admin import BaseView
from flask_admin import expose
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from uuid import uuid4
from datetime import datetime
from time import time
from flask import url_for, redirect, render_template, request
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers
from werkzeug.security import generate_password_hash, check_password_hash
import tablib


def uuid():
    return uuid4().hex


def onupdate_time():
    return int(time())


db = SQLAlchemy()
app = Flask(__name__)
babel = Babel(app)
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'united'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
# ## 连接数据库
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://supercloud_web:Zyadmin@123@10.0.0.29:3306/supercloud?charset=UTF8MB4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456790'
#
# # 06_展示数据库表单新增
db.init_app(app)


# 07_新增登陆界面：将原来的UserAdmin表改为User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    # password = fields.StringField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        # if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):

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
    form_excluded_columns = ['collector_product_maps', 'metric_types', 'database_global_tags', 'uuid', 'create_time',
                             'update_time', 'is_deleted', 'delete_time']


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            # user.password = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# 数据库产品表
class DatabaseTypes(db.Model):
    __tablename__ = 'database_types'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), comment='数据库产品名')
    cloud_based_only = db.Column(db.String(255), comment='云数据库 是/否')
    paltform = db.Column(db.String(255), comment='数据库平台')
    os_type = db.Column(db.String(255), comment='操作系统类型')
    db_version = db.Column(db.String(13, 2), comment='数据库版本')
    db_series = db.Column(db.String(255), comment='产品系列')
    db_class = db.Column(db.String(255), comment='产品大类')
    db_engine = db.Column(db.String(255), comment='数据库引擎')
    db_model = db.Column(db.String(13, 2), comment='数据库模型')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)

    collector_product_maps = db.relationship("CollectorProductMap", backref="数据库产品名")

    def __repr__(self):
        result = []
        for i in (self.id, self.product_name, self.paltform, self.os_type, self.db_version):
            if i:
                result.append(str(i))
            else:
                continue
        return ','.join(result)


class MyV_DT(MyModelView):
    column_labels = {
        'id': u'编号',
        'product_name': u'数据库产品名',
        'cloud_based_only': u'云数据库',
        'paltform': u'平台',
        'os_type': u'操作系统类型',
        'db_version': u'数据库版本',
        'db_series': u'产品系列',
        'db_class': u'产品大类',
        'db_engine': u'引擎',
        'db_model': u'模型',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'product_name', 'cloud_based_only', 'paltform',
                   'db_series', 'db_class', 'os_type', 'db_version',
                   'db_engine', 'db_model', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'product_name', 'cloud_based_only', 'paltform',
        'db_series', 'db_class', 'os_type', 'db_version',
        'db_engine', 'db_model', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'cloud_based_only': [
            ('是', '是'),
            ('否', '否'),
        ],
        'paltform': [
            ('自建', '自建'),
            ('Aliyun', 'Aliyun'),
            ('Amazon', 'Amazon'),
            ('Azure', 'Azure'),
            ('Tencent', 'Tencent'),
        ],
    }


# 采集器表
class CollectorProduct(db.Model):
    __tablename__ = 'collector_product'
    collector_id = db.Column(db.Integer, primary_key=True, comment='采集器编号')
    collector_name = db.Column(db.String(255), comment='采集器名称')
    product_type = db.Column(db.String(255), comment='数据库生产类型')
    product_steps = db.Column(db.String(255), comment='生产步骤')
    envir_prepar = db.Column(db.Integer, comment='环境准备')
    metrics_sort = db.Column(db.Integer, comment='指标梳理')
    dev_schedule = db.Column(db.Integer, comment='研发进度')
    test_schedule = db.Column(db.Integer, comment='测试进度')
    document_delivery = db.Column(db.Integer, comment='文档交付')
    info = db.Column(db.String(255), comment='说明')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)

    collector_product_maps = db.relationship("CollectorProductMap", backref="采集器名称")
    metric_types = db.relationship("MetricTypes", backref="采集器名称")
    database_global_tags = db.relationship("DatabaseGlobalTags", backref="采集器名称")

    def __repr__(self):
        result = []
        for i in (self.collector_id, self.collector_name):
            if i:
                result.append(str(i))
            else:
                continue
        return ','.join(result)


class MyV_CP(MyModelView):
    column_labels = {
        'collector_id': u'采集器编号',
        'collector_name': u'采集器名称',
        'product_type': u'数据库生产类型',
        'product_steps': u'生产步骤',
        'envir_prepar': u'环境准备(%)',
        'metrics_sort': u'指标梳理(%)',
        'dev_schedule': u'研发进度(%)',
        'test_schedule': u'测试进度(%)',
        'document_delivery': u'文档交付(%)',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = (
        'collector_id', 'collector_name', 'product_type', 'product_steps',
        'envir_prepar', 'metrics_sort',
        'dev_schedule', 'test_schedule', 'document_delivery', 'create_time', 'update_time')
    # 指定可排序的列
    column_filters = (
        'collector_id', 'collector_name', 'product_type', 'product_steps',
        'envir_prepar', 'metrics_sort',
        'dev_schedule', 'test_schedule', 'document_delivery', 'create_time', 'update_time')
    # 下拉框选择
    form_choices = {
        'product_type': [
            ('数据生产A', '数据生产A'),
            ('数据生产B', '数据生产B'),
        ],
        'product_steps': [
            ('研发进度-环境准备-测试部署-指标梳理-交付文档', '研发进度-环境准备-测试部署-指标梳理-交付文档'),
            ('环境准备-指标梳理-研发进度-测试部署-交付文档', '环境准备-指标梳理-研发进度-测试部署-交付文档'),
        ],
        'envir_prepar': [
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
        'metrics_sort': [
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
        'dev_schedule': [
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
        'test_schedule': [
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
        'document_delivery': [
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
    }


# 采集器与产品映射表
class CollectorProductMap(db.Model):
    __tablename__ = 'collector_product_map'
    id = db.Column(db.Integer, primary_key=True)
    collector_id = db.Column(db.Integer, comment='采集器编号')
    product_id = db.Column(db.Integer, comment='数据库产品编号')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, db.ForeignKey('database_types.id'))
    collector_id = db.Column(db.Integer, db.ForeignKey('collector_product.collector_id'))


class MyV_CPM(MyModelView):
    column_labels = {
        'id': u'编号',
        'collector_id': u'采集器编号',
        'collector_product.collector_name': '采集器',
        'product_id': u'数据库产品编号',
        'database_types.product_name': '数据库产品',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = (
        'id', 'collector_id',  'product_id',
        'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = (
        'id', 'collector_id', 'product_id',
        'create_time', 'update_time')


# 指标类型表
class MetricTypes(db.Model):
    __tablename__ = 'metric_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), comment='指标类型')
    type_info = db.Column(db.String(255), comment='类型说明')
    status = db.Column(db.String(255), default='待审核', comment='指标类型开发状态 例如：待审核 已审核 需更新 完成')
    info = db.Column(db.String(255), comment='说明')
    collector_id = db.Column(db.Integer, comment='采集器编号')
    sql_text = db.Column(db.Text, comment='SQL语句')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)
    collector_id = db.Column(db.Integer, db.ForeignKey('collector_product.collector_id'))


class MyV_MT(MyModelView):
    column_labels = {
        'id': u'编号',
        'type': u'指标类型',
        'type_info': u'类型说明',
        'status': '开发状态',
        'info': '备注',
        'collector_id': u'采集器编号',
        'sql_text': u'SQL语句',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = (
        'id', 'type', 'type_info', 'status', 'info', 'collector_id',
        'sql_text', 'create_time', 'update_time')
    # 指定可排序的列
    column_filters = (
        'id', 'type', 'type_info', 'status', 'info', 'collector_id',
        'sql_text', 'create_time', 'update_time')

    # 下拉框选择
    form_choices = {
        'status': [
            ('待审核', '待审核'),
            ('已审核', '已审核'),
            ('需更新', '需更新'),
            ('完成', '完成'),
        ],
    }

# 全局标签表
class DatabaseGlobalTags(db.Model):
    __tablename__ = 'database_global_tags'
    id = db.Column(db.Integer, primary_key=True)
    collector_id = db.Column(db.Integer, comment='采集器编号')
    tag_name = db.Column(db.String(255), comment='标签名')
    info = db.Column(db.String(255), comment='说明')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)
    collector_id = db.Column(db.Integer, db.ForeignKey('collector_product.collector_id'))


class MyV_DGT(MyModelView):
    column_labels = {
        'id': u'编号',
        'collector_id': u'采集器编号',
        'tag_name': u'标签名',
        'info': u'说明',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = ('id', 'collector_id', 'tag_name', 'info', 'create_time', 'update_time')
    # 指定可过滤的列
    column_filters = ('id', 'collector_id', 'tag_name', 'info', 'create_time', 'update_time')


user = {
    'username': '此页面为自定义页面案例',
    'bio': 'Focus on the principle, technology and application of data management technology',
}
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


# 指标明细表
class MetricInfo(db.Model):
    __tablename__ = 'metric_info'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, comment='类型编号')
    metric = db.Column(db.String(255), comment='指标')
    data_type = db.Column(db.String(255), comment='数据类型')
    unit = db.Column(db.String(255), comment='单位')
    is_tag = db.Column(db.String(255), comment='是否为Tag 是/否')
    comment = db.Column(db.String(255), comment='描述')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)


class MyV_MI(MyModelView):
    column_labels = {
        'id': u'编号',
        'type_id': u'类型编号',
        'metric': u'指标',
        'data_type': u'数据类型',
        'unit': u'单位',
        'is_tag': u'是否为Tag 是/否',
        'comment': u'描述',
        'create_time': u'创建时间',
        'update_time': u'修改时间'
    }
    column_list = (
        'id', 'type_id', 'metric', 'data_type', 'unit', 'is_tag',
        'comment', 'create_time', 'update_time')
    # 指定可排序的列
    column_filters = (
        'id', 'type_id', 'metric', 'data_type', 'unit', 'is_tag',
        'comment', 'create_time', 'update_time')


# Flask views
@app.route('/')
def index():
    return render_template('index.html')


class Happy(BaseView):
    @expose('/')
    def index(self):
        return self.render('happy.html', user=user, movies=movies)


# Initialize flask-login
init_login()
admin = Admin(app, name='SuperCloud', index_view=MyAdminIndexView(), base_template='my_master.html',
              template_mode='bootstrap3')

admin.add_view(MyV_DT(DatabaseTypes, db.session, name=u'数据库产品表', category="数据库与采集器"))
admin.add_view(MyV_CP(CollectorProduct, db.session, name=u'采集器生产表', category="数据库与采集器"))
admin.add_view(MyV_CPM(CollectorProductMap, db.session, name=u'采集器和数据库产品映射关系表', category="数据库与采集器"))
admin.add_view(MyV_MT(MetricTypes, db.session, name=u'指标类型表', category="指标与标签"))
admin.add_view(MyV_MI(MetricInfo, db.session, name=u'指标明细表', category="指标与标签"))
admin.add_view(MyV_DGT(DatabaseGlobalTags, db.session, name=u'全局标签表', category="指标与标签"))

admin.add_view(Happy(name=u'自定义页面'))
# admin.add_view(MyModelView(User, db.session, name=u'用户管理'))

app.run(debug=True, host='0.0.0.0', port=5000)
