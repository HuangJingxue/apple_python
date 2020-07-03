# -*- coding:utf8 -*-
from config import DevConfig
from flask import Flask
from flask_admin import Admin
from flask_admin import BaseView
from flask_admin import expose
from flask_babelex import Babel
from flask import url_for, redirect, render_template, request
from flask import send_file, send_from_directory
import os
from flask import make_response


import models
import views

from core_app import get_data_ana
from core_app import get_collect_info
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

db = models.db
app = Flask(__name__)

# 开发环境
app.config.from_object(DevConfig)
bel = Babel(app)
db.init_app(app)
models.init_login(app)


# Flask views
@app.route('/')
def index():
    return render_template('index.html')

# core-app连接数据库的通用参数
params = {
    'url': DevConfig.URL,
    'port': DevConfig.PORT,
    'username': DevConfig.USERNAME,
    'password': DevConfig.PASSWORD,
    'dbname': DevConfig.DBNAME,
    'engine': DevConfig.ENGINE,
}

class Happy(BaseView):
    @expose('/')
    def index(self):
        params_ana = params
        params_ana['info'] = ['total_ana','collectors'
                              ]
        user = {
            'username': '驾驶舱',
            'bio': 'Focus on metrics, dashboards and alerts of databases',
        }
        data = get_data_ana.startup(**params_ana)
        return self.render('status.html', user=user, data=data)

class HelpYourSelf(BaseView):
    @expose('/', methods=('POST', 'GET'))
    def index(self):
        if request.method == 'POST':
            params_help = {
                'url': DevConfig.URL,
                'port': DevConfig.PORT,
                'username': DevConfig.USERNAME,
                'password': DevConfig.PASSWORD,
                'dbname': DevConfig.DBNAME,
                'engine': DevConfig.ENGINE,
                'collectors': request.form.getlist("check_box_list"),
                'out_type': request.form.get('output'),
            }
            filename = get_collect_info.startup(**params_help)
            directory = os.getcwd()
            response = make_response(send_from_directory(directory, filename, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                filename.encode().decode('latin-1'))
            return response
            # return '@@@'.join(checkbox)
        elif request.method == 'GET':
            _params = params
            _params['info'] = ['collectors']
            data = get_data_ana.startup(**_params)
            return self.render('help_yourself.html', data=data)
        else:
            return 'Error'

# Initialize flask-login
admin = Admin(app, name='QingYu', index_view=models.MyAdminIndexView(), base_template='my_master.html',
              template_mode='bootstrap3')

#admin.add_view(views.MyV_RE(models.Read, db.session, name=u'阅读', category="自律给我自由"))
#admin.add_view(views.MyV_BB(models.BodyBuilding, db.session, name=u'健身', category="自律给我自由"))
admin.add_view(views.MyV_FC(models.FinancialChannel, db.session, name=u'理财渠道', category="理财就是理生活"))
admin.add_view(views.MyV_FT(models.FinancialType, db.session, name=u'理财类型', category="理财就是理生活"))
admin.add_view(views.MyV_FI(models.FinancialInfo, db.session, name=u'理财明细', category="理财就是理生活"))
admin.add_view(Happy(name=u'驾驶舱'))
admin.add_view(HelpYourSelf(name=u'自助中心'))
app.run(debug=True, host='0.0.0.0', port=5000)
