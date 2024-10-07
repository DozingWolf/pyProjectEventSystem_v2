from flask import request
from flask.blueprints import Blueprint,current_app
from flask.helpers import make_response
from loguru import logger
from traceback import format_exc

from .dataTranser import getCurrentTimeFormatString

# 系统初始化功能，建立一个系统管理员，并生成系统最基础的配置信息，生成一个用于修改的基础公司和基础部门
# 感觉这个功能应该独立出来，不放在Flask里面，否则需要鉴权的话就是一个悖论功能，考虑一下，移出来
sysInitialBP = Blueprint('SysInitial',__name__)

@sysInitialBP.route('/SysInitial',methods=['POST'])
def sysInitial():
    # 初始化管理员用户
    createUserSql = '''
                    INSERT INTO TMSTUSER
                    (empid,empcode, empname, passwd, sex, 
                     createuser,createdate, modifyuser, modifydate, status)
                    VALUES
                    (?, ?, ?, ?, ?, 
                     ?, ?, ?, ?, 0);
                    '''
    sqlParam = (0,'0000','Admin','123123',0,0,getCurrentTimeFormatString(),0,getCurrentTimeFormatString())
    cursor = current_app.conn.cursor()
    try:
        cursor.execute(createUserSql,sqlParam)
        current_app.conn.commit()
        rtnMsg = {'code':2000,'msg':'success'}
        return make_response(rtnMsg)
    except Exception as e:
        logger.error(format_exc())
        rtnMsg = {'code':4000,'msg':'fail'}
        return make_response(rtnMsg)
    # 初始化配置
    # 初始化公司
    # 初始化部门