from flask import request,session
from flask.blueprints import Blueprint,current_app
from flask.helpers import make_response
from loguru import logger
from traceback import format_exc
# 加载一些自己写的方法
from .dataTranser import getCurrentTimeFormatString
from .backendErrorList import EmptyJsonValue,ErrorJsonData,NoneJsonKey

userActionBP = Blueprint('User',__name__)

# 创建用户接口
@userActionBP.route('/CreateUser',methods=['POST'])
def createUser():
    # 定义创建用户SQL语句
    # 因为使用了sqlite，所以不能使用类似oracle的sequence，先用自增字段来代替下
    createUserSql = '''
                    INSERT INTO TMSTUSER
                    (empcode, empname, passwd, sex, 
                     createuser,createdate, modifyuser, modifydate, status)
                    VALUES
                    (?, ?, ?, ?, 
                     ?, ?, ?, ?, 0);
                    '''
    # 获取head中current user信息
    currentUser = session.get('currentUser')
    logger.info(currentUser)
    # 接受前端传递的json变量
    jsonData = request.get_json()
    logger.info(jsonData)
    # 校验前端传参，确认每个值都合法，否则返回错误信息
    try:
        if 'empcode' not in jsonData.keys():
            raise NoneJsonKey(message='miss key column!',keycolumn='empcode')
        if jsonData['empcode'] == '':
            raise EmptyJsonValue(message='empcode is null!',keycolumn='empcode')
        if 'empname' not in jsonData.keys():
            raise NoneJsonKey(message='miss key column!',keycolumn='empname')
        if jsonData['empname'] == '':
            raise EmptyJsonValue(message='empname is null!',keycolumn='empname')
        if 'passwd' not in jsonData.keys():
            raise NoneJsonKey(message='miss key column!',keycolumn='passwd')
        if jsonData['passwd'] == '':
            raise EmptyJsonValue(message='passwd is null!',keycolumn='passwd')
        if 'sex' not in jsonData.keys():
            raise NoneJsonKey(message='miss key column!',keycolumn='sex')
        if jsonData['sex'] == '':
            raise EmptyJsonValue(message='sex is null!',keycolumn='sex')
        if jsonData['sex'] not in (0,1):
            raise ErrorJsonData(message='error value!',keycolumn='sex',send=jsonData['sex'])
    except NoneJsonKey as e:
        rtnMsg = {'code':e.code,'msg':'%s is required'%e.errorColumn}
        return make_response(rtnMsg)
    except EmptyJsonValue as e:
        rtnMsg = {'code':e.code,'msg':'%s is null'%e.errorColumn}
        return make_response(rtnMsg)
    except ErrorJsonData as e:
        rtnMsg = {'code':e.code,'msg':'%s got a error value %s'%(e.errorColumn,e.errorValue)}
        return make_response(rtnMsg)
    except Exception as e:
        logger.error(format_exc())
        rtnMsg = {'code':4000,'msg':'failed,check logfile'}
        return make_response(rtnMsg)
    # 校验前端传参，确认每个值都合法，否则返回错误信息
    # 取出json中的empcode、empname、passwd、sex信息并赋予变量
    empcode = jsonData['empcode']
    empname = jsonData['empname']
    passwd = jsonData['passwd']
    sex = jsonData['sex']
    createuser = currentUser
    modifyuser = currentUser
    createdate = getCurrentTimeFormatString()
    modifydate = getCurrentTimeFormatString()
    logger.info('user code is %s,user name is %s,user passwd is %s,sex is %r,current user is %s'%(empcode,empname,passwd,sex,createuser))
    # 执行绑定变量的sql语句
    cursor = current_app.conn.cursor()
    try:
        cursor.execute(createUserSql,(empcode,empname,passwd,sex,createuser,createdate,modifyuser,modifydate))
        current_app.conn.commit()
        rtnMsg = {'code':2000,'msg':'success'}
        return make_response(rtnMsg)
    except Exception as e:
        logger.error(format_exc())
        rtnMsg = {'code':4000,'msg':'failed ,check logfile'}
        return make_response(rtnMsg)

@userActionBP.route('/EditUser',methods=['POST'])
def editUser():
    # 修改人员信息，允许修改的字段为empname、passwd、sex、status
    pass

@userActionBP.route('/QueryUser',methods=['GET'])
def queryUser():
    pass

