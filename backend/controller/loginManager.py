from flask import request,session
from flask.blueprints import Blueprint,current_app
from flask.helpers import make_response
from traceback import format_exc
from loguru import logger

from .dataQualityChecker import isExistCheck,isEmptyCheck
from .backendErrorList import EmptyJsonValue,ErrorJsonData,NoneJsonKey



loginManagerBP = Blueprint('login',__name__)

@loginManagerBP.route('/login',methods=['POST'])
def login():
    if session.get('logged_in') is True:
        rtnMsg = {'code':2000,'msg':'already logged in'}
        return make_response(rtnMsg)
    try:
        # 定一个变量检查清单
        jsonKeyCheckList = ['empcode','passwd','verifycode']
        jsonValueNotNullCheckList = ['empcode','passwd','verifycode']
        jsonData = request.get_json()
        logger.info(jsonData)
        # 检查json中是否存在empcode,passwd,verifycode三个key
        isExistCheck(model=jsonKeyCheckList,data=jsonData)
        # 检查empcode,passwd,verifycode三个key是否为空
        isEmptyCheck(model=jsonValueNotNullCheckList,data=jsonData)

        session['logged_in'] = True
        session['currentUser'] = jsonData['empcode']
        rtnMsg = {'code':2000,'msg':'login success'}
        return make_response(rtnMsg)
    except NoneJsonKey as e:
        rtnMsg = {'code':e.code,'msg':'%s is required'%e.errorColumn}
        return make_response(rtnMsg)
    except EmptyJsonValue as e:
        rtnMsg = {'code':e.code,'msg':'%s is null'%e.errorColumn}
        return make_response(rtnMsg)
    except Exception as e:
        logger.error(format_exc())
        rtnMsg = {'code':5000,'msg':'server error, check logfile'}

        return make_response(rtnMsg)





