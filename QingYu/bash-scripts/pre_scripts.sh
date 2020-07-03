#  部署文档
# 1. 安装依赖关系包
pip install -r requirements.txt
# 2. 拷贝定制的css到flask_admin目录下 注意不通的服务器的第三安装包的位置可能不同
cp css-backup/united/bootstrap.min.css venv/lib/python3.7/site-packages/flask_admin/static/bootstrap/bootstrap3/swatch/united
mv venv/lib/python3.7/site-packages/flask_admin/templates/bootstrap3 venv/lib/python3.7/site-packages/flask_admin/templates/bootstrap3.bac
mv css-backup/bootstrap3 venv/lib/python3.7/site-packages/flask_admin/templates/

# hexo
curl -sL https://rpm.nodesource.com/setup_14.x | bash -
yum install -y nodejs
npm install -g hexo-cli

