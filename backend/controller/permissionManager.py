from flask import request,session
from flask.blueprints import Blueprint,current_app
from flask.helpers import make_response
from traceback import format_exc
from loguru import logger
from time import time

from .dataQualityChecker import isExistCheck,isEmptyCheck
from .backendErrorList import EmptyJsonValue,ErrorJsonData,NoneJsonKey,VerifyCodeError,VerifyTimeoutError

permissionManagerBP = Blueprint('permissionManager',__name__)

@permissionManagerBP.route('/QueryUserPermission',methods=['POST'])
def queryUserPermission():
    rtnMsg = make_response({'code':2000,'msg':'success','pdict':{}})
    
    pass

def coreQueryUserPermission(usercode:str)->dict:
    rtnPermissionDict = {}

    return rtnPermissionDict