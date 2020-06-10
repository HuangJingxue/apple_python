# -*- coding:utf8 -*-
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

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

# 汉化处理
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'united'

# ## 连接数据库
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myweb:myweb@127.0.0.1:3306/myweb?charset=UTF8MB4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456790'
#
# # 展示数据库表单新增
db.init_app(app)


# 新增登陆界面：将原来的UserAdmin表改为User
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
    can_delete = False
    # 导出功能
    can_export = True
    export_types = ['csv']
    # 不显示的列
    column_exclude_list = ['uuid', 'is_deleted', 'delete_time']
    # 不创建也不编辑的列
    form_excluded_columns = ['collector_product_maps', 'metric_types', 'database_global_tags', 'uuid', 'create_time', 'update_time', 'is_deleted', 'delete_time']


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



class BusinessRequire(db.Model):
    __tablename__ = 'business_require'
    id = db.Column(db.Integer, primary_key=True)
    business = db.Column(db.String(255), comment='业务名')
    requires = db.Column(db.String(255), comment='业务需求')
    requires_sql = db.Column(db.String(255), comment='业务需求SQL')
    requestor = db.Column(db.String(255), comment='需求人')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)



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
admin = Admin(app, name='QingYu', index_view=MyAdminIndexView(), base_template='my_master.html',
              template_mode='bootstrap3')

admin.add_view(MyV_BR(BusinessRequire, db.session, name=u'业务需求表', category="业务需求"))

#admin.add_view(Happy(name=u'自定义页面'))
# admin.add_view(MyModelView(User, db.session, name=u'用户管理'))

app.run(debug=True, host='192.168.206.139', port=5000)
