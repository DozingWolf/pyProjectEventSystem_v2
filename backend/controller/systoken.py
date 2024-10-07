from time import time
from flask import Blueprint, current_app, request
from flask.helpers import make_response
from jwt import encode as jwtencode
from jwt import decode as jwtdecode
from controller.markIP import markUserIP
from controller.errorlist import AuthNoUserError,AuthDupUserError
from model import db

systokenBP = Blueprint('systokenBP',__name__)

@systokenBP.route('/createtoken',methods=['POST'])
def createTokenUri():
    current_app.logger.info(markUserIP())
    getData = request.form
    userId = getData.get('uid')
    userName = getData.get('uname')
    pwhash = getData.get('pwhs')
    hashValue = createToken(uid=userId,uname=userName,pwhs=pwhash)
    return make_response(hashValue)

def createToken(uid:int,uname:str,pwhs:str):
    try:
        if uid is None:
            raise AttributeError('authToken args uid was empty')
        if uname is None:
            raise AttributeError('authToken args uname was empty')
        if pwhs is None:
            raise AttributeError('authToken args pwhs was empty')
        selectSQL = 'select username from IntfUser where userid = :uid and username = :uname and userpw = :upw'
        selectPara = {'uid':uid,'uname':uname,'upw':pwhs}
        tokenUser = db.session.execute(selectSQL,selectPara).fetchall()
        if len(tokenUser) == 0:
            raise AuthNoUserError('username or password error')
        elif len(tokenUser) > 1:
            raise AuthDupUserError('duplicate user')
        rtnData = jwtencode(payload={'userid':uid,
                                     'username':uname,
                                     'passwordhash':pwhs,
                                     'exp':time()+72000},
                            key=current_app.hashkey,
                            algorithm='HS256')
        current_app.logger.debug('token is :%s'%rtnData)
        updateSQL = 'update IntfUser set usertk = :tk where userid = :uid and username = :uname and userpw = :upw'
        updatePara = {'tk':rtnData,'uid':uid,'uname':uname,'upw':pwhs}
        db.session.execute(updateSQL,updatePara)
        db.session.commit()
        current_app.logger.debug('an user got a sys token success')
        return {'errorflag':0,'token':rtnData}
    except AttributeError as err:
        current_app.logger.exception(err)
        errorMsg = {'errorflag':-1,'errormsg':'no authToken function args, please check it again, u can check log file'}
        return errorMsg
    except AuthNoUserError as err:
        current_app.logger.exception(err)
        errorMsg = {'errorflag':-1,'errormsg':'no user or password error'}
        return errorMsg
    except AuthDupUserError as err:
        current_app.logger.exception(err)
        errorMsg = {'errorflag':-1,'errormsg':'duplicate user'}
        return errorMsg
    except Exception as err:
        current_app.logger.exception(err)
        errorMsg = {'errorflag':-1,'errormsg':'something was error, see log file'}
        return errorMsg

@systokenBP.route('/solutiontoken',methods=['POST'])
def solutionTokenUri():
    current_app.logger.info(markUserIP())
    getData = request.form
    sToken = getData.get('token')
    rtnData = solutionToken(tk=sToken)
    return rtnData

def solutionToken(tk:str):
    try:
        if tk is None:
            raise AttributeError
        solutionData = jwtdecode(jwt=tk,
                                 key=current_app.hashkey,
                                 algorithms='HS256')
        current_app.logger.debug('user have solutioned a token data')
        return solutionData
    except Exception as err:
        current_app.logger.exception(err)
        errorMsg = {'errorflag':-1,'errormsg':'something was error, see log file'}
        return errorMsg