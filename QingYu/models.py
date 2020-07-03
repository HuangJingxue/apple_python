# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from uuid import uuid4
from datetime import datetime
from time import time
from flask_admin import expose
from flask import url_for, redirect, render_template, request
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


def uuid():
    return uuid4().hex


def onupdate_time():
    return int(time())


db = SQLAlchemy()

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

# 阅读
class Read(db.Model):
    __tablename__ = 'read'
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

# 健身
class BodyBuilding(db.Model):
    __tablename__ = 'bbuilding'
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

# 理财渠道
class FinancialChannel(db.Model):
    __tablename__ = 'fchannel'
    id = db.Column(db.Integer, primary_key=True)
    channelname = db.Column(db.String(255), comment='渠道名称')
    info = db.Column(db.String(255), comment='说明')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)

    fchannels = db.relationship("FinancialInfo", backref="fchannel")


    def __repr__(self):
        result = []
        for i in (self.id, self.channelname):
            if i:
                result.append(str(i))
            else:
                continue
        self.new_name = ','.join(result)
        return self.new_name


# 理财类型
class FinancialType(db.Model):
    __tablename__ = 'ftype'
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(255), comment='类型名称')
    info = db.Column(db.String(255), comment='说明')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)
    ftypes = db.relationship("FinancialInfo", backref="ftype")

    def __repr__(self):
        result = []
        for i in (self.id, self.typename):
            if i:
                result.append(str(i))
            else:
                continue
        self.new_name = ','.join(result)
        return self.new_name


# 理财明细
class FinancialInfo(db.Model):
    __tablename__ = 'finfo'
    id = db.Column(db.Integer, primary_key=True)
    channelid = db.Column(db.Integer, comment='渠道ID')
    typeid = db.Column(db.Integer, comment='类型ID')
    fundname = db.Column(db.String(255), comment='基金名称')
    amount = db.Column(db.Integer, comment='金额')
    status = db.Column(db.String(255), comment='状态')
    info = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='修改时间')
    uuid = db.Column(db.String(32), default=uuid, unique=True, comment='UUID')
    is_deleted = db.Column(db.Integer)
    delete_time = db.Column(db.DateTime)
    channelid = db.Column(db.Integer, db.ForeignKey('fchannel.id'))
    typeid = db.Column(db.Integer, db.ForeignKey('ftype.id'))

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
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

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
