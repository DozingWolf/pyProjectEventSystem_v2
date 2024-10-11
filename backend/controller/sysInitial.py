from loguru import logger
from traceback import format_exc
from sqlite3 import connect

from .dataTranser import getCurrentTimeFormatString
from .dataEncrypt import TraditionalPassword

# 系统初始化功能，建立一个系统管理员，并生成系统最基础的配置信息，生成一个用于修改的基础公司和基础部门
# 感觉这个功能应该独立出来，不放在Flask里面，否则需要鉴权的话就是一个悖论功能，考虑一下，移出来

def sysInitial():
    
    createUserSql = '''
                    INSERT INTO TMSTUSER
                    (empid,empcode, empname, passwd, sex, 
                     createuser,createdate, modifyuser, modifydate, status)
                    VALUES
                    (?, ?, ?, ?, ?, 
                     ?, ?, ?, ?, 0);
                    '''
    try:
        sysCipher = TraditionalPassword()
        sqlParam = (0,'0000','Admin',sysCipher.encryptPassword(passwd='admin@123'),0,0,getCurrentTimeFormatString(),0,getCurrentTimeFormatString(),)
        conn = connect(database='./db/backendModelBD',check_same_thread=False)
        cursor = conn.cursor()
    
        # 初始化管理员用户
        cursor.execute(createUserSql,sqlParam)
        conn.commit()
        # 公私钥
        sysCipher.generateRSAKeyPair()
        rtnMsg = {'code':2000,'msg':'success'}
    except Exception as e:
        logger.error(format_exc())
        rtnMsg = {'code':4000,'msg':'fail'}
    # 初始化配置信息

    # 初始化公司
    # 初始化部门