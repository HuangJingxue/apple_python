class Config(object):
    """Base config class."""
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    FLASK_ADMIN_SWATCH = 'united'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456790'
    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    """Production config class."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root123@127.0.0.1:3306/myweb?charset=UTF8MB4'


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root123@127.0.0.1:3306/myweb?charset=UTF8MB4'
    URL = '127.0.0.1'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = 'root123'
    DBNAME = 'myweb'
    ENGINE = 'mysql'
