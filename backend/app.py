# import Flask
from flask import Flask
from flask.blueprints import Blueprint
# import blueprint
from controller.loginManager import loginManagerBP
from controller.sysInitial import sysInitialBP
from controller.userAction import userActionBP
# import config
from configparser import ConfigParser
# import log
from loguru import logger

app = Flask(__name__)

# initial log and dblink
param = ConfigParser()
param.read('./conf/conf.ini')
if len(param.sections()) == 0:
    logger.critical('配置文件backend.conf不存在')
    exit()
app.runningConfig = param
# check parameter
if bool(param['DB']['sqlite']) is True:
    from sqlite3 import connect
    app.conn = connect(database=param['DB']['sqlite_file'],check_same_thread=False)
else:
    logger.critical('演示环境，其他DB连接我懒得实现，别试了')
    exit()
# initial session secret key
app.config['SECRET_KEY'] = param['Flask']['secret_key']

# register blueprint
app.register_blueprint(blueprint=loginManagerBP,url_prefix='/api/v1.0')
app.register_blueprint(blueprint=sysInitialBP,url_prefix='/api/v1.0')
app.register_blueprint(blueprint=userActionBP,url_prefix='/api/v1.0/User')


if __name__ == '__main__':
    app.run(port=80,debug=True)