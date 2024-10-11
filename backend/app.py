# import Flask
from flask import Flask
from flask.blueprints import Blueprint
# import blueprint
from controller.loginManager import loginManagerBP
from controller.userAction import userActionBP
# import self cipher
from controller.dataEncrypt import TraditionalPassword
# import config
from configparser import ConfigParser
# import log
from loguru import logger
# from flask_loguru import logger

app = Flask(__name__)

# initial config, log and dblink
param = ConfigParser()
param.read('./conf/conf.ini')
if len(param.sections()) == 0:
    logger.critical('配置文件backend.conf不存在')
    exit()
app.runningConfig = param

logger.debug(param['Flask']['log_rotation'])
logger.add(param['Flask']['log'],
           rotation=param['Flask']['log_rotation'],
           compression=param['Flask']['log_compression'],
           level=param['Flask']['log_level'])

# check parameter
if bool(param['DB']['sqlite']) is True:
    from sqlite3 import connect
    app.conn = connect(database=param['DB']['sqlite_file'],check_same_thread=False)
else:
    logger.critical('演示环境，其他DB连接我懒得实现，别试了')
    exit()

# load public and private key
try:
    with open('./key/publicKey.pem','rb') as f:
        RSA2048PublicKey = f.read()
    with open('./key/privateKey.pem','rb') as f:
        app.RSA2048PrivateKey = f.read()
    app.sysChiper = TraditionalPassword()
    app.sysChiper.new(RSA2048PublicKey)
    del RSA2048PublicKey
except FileNotFoundError as e:
    logger.critical('私钥文件privateKey.pem不存在')
    exit()
# initial session secret key
app.config['SECRET_KEY'] = param['Flask']['secret_key']

# register blueprint
app.register_blueprint(blueprint=loginManagerBP,url_prefix='/api/v1.0')
app.register_blueprint(blueprint=userActionBP,url_prefix='/api/v1.0/User')


if __name__ == '__main__':
    app.run(port=80,debug=True)
