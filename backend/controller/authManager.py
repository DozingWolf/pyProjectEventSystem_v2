from functools import wraps
from flask import current_app,request,session,Blueprint
from time import time
from werkzeug.security import check_password_hash
from traceback import print_exc
from model import db
from model.user import User
from tool.responseGenerator import responseStructures,responseStructureswithCookie
from tool.dataTranser import b64TransString
from controller.errorlist import AuthNoPermissionError,AuthError,DBDataError

authManagerBP = Blueprint('authUser',__name__)
# 现在的登录设置已经满足普通web的登录要求
# 考虑下微信小程序的需求，需要建立一套支持微信自定义登录认证方式的接口
# 同时需要考虑对普通web和微信登录的兼容性
# 可能要考虑使用JWT的Token功能，那这样对原有的web认证方式冲击比较大

@authManagerBP.route('/loginUser',methods=['POST'])
def loginUser():
    if session.get('logged_in') is True:
        return responseStructures(rstatus='200',
                                  rbody={'error_code':2000,
                                         'error_msg':'u have already login by account %s'%session.get('user_name')})                               
    rtnMsg = ''
    loginTime = time()
    try:
        # 检查入参情况
        loginPara = request.get_json()
        if loginPara is None:
            rtnMsg = 'No login para input'
            current_app.logger.error(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='userid, username, passwd')
        if 'userid' in loginPara:
            current_app.logger.debug('userid %s'%loginPara['userid'])
        else:
            rtnMsg = 'No userid'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='userid')
        if 'username' in loginPara:
            current_app.logger.debug('username %s'%loginPara['username'])
        else:
            rtnMsg = 'No username'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='username')
        if 'passwd' in loginPara:
            current_app.logger.debug('passwd %s'%loginPara['passwd'])
        else:
            rtnMsg = 'No passwd'
            current_app.logger.info(rtnMsg)
            raise AuthError(message=rtnMsg,arguname='passwd')
    except AuthError as err:
        return responseStructures(rstatus=err.code,
                                  rbody={'error_code':err.error_code,
                                         'error_msg':err.message,
                                         'args':err.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    # 开始查询并验证用户信息
    # 构造验证用户sql
    current_app.logger.debug('start makr query sql')
    countNumSQL = '''select count(1) from edm_test_schema.tmstuser t 
                     where 1=1 
                       and t.username = :username  
                       and t.userid = :userid'''
    countNumPara = {'username':loginPara['username'],
                    'userid':loginPara['userid']}
    # 构造获取用户权限sql
    selectUserSql = 'select isadmin, passwd from edm_test_schema.tmstuser where userid = :userid'
    selectUserPara = {'userid':loginPara['userid']}
    selectPerSql = '''select 
                      u.userid ,u.username ,up.permissionmemo ,p.permissionid ,p.permissionname ,
                      p.urlitem
                      from edm_test_schema.tmstuser u
                      inner join edm_test_schema.tmstuserpermission up on u.userid  = up.userid 
                      inner join edm_test_schema.tmstpermission p on up.permissionid  = p.permissionid 
                      where 1=1 
                        and u.status = 0
                        and up.status = 0
                        and p.status = 0
                        and u.userid = :userid
    '''
    selectPerPara = {'userid':loginPara['userid']}
    # 开始执行查询
    try:
        current_app.logger.debug('start execute sql')
        countExeSql = db.session.execute(countNumSQL,countNumPara)
        countRtn = countExeSql.fetchall()
        current_app.logger.debug('query result is :')
        current_app.logger.debug(countRtn)
        if countRtn[0][0] == 1:
            # 对用户进行密码获取
            # 同步将一些其他数据也先取出，减少后续DB查询次数
            getDBPasswd = db.session.execute(selectUserSql,selectUserPara)
            getDBPasswdRtn = getDBPasswd.fetchall()
            # 加入用户密码校验
            # 先将base64字符串转换为提交的密码
            current_app.logger.debug('b64 passwd is : %s'%loginPara['passwd'])
            userPw = b64TransString(input=loginPara['passwd'])
            # 将加密后的密码与数据库取出的数据进行比对
            if check_password_hash(pwhash = getDBPasswdRtn[0][1],password = userPw):
                # 如果一致则建立用户对象
                current_app.logger.debug('password match')
                newUser = User(userid=loginPara['userid'],username=loginPara['username'],pcode='001',logintime=loginTime)
            else:
                # 如果不一致反馈401错误
                current_app.logger.debug('password mismatch')
                raise AuthError(message='password mismatch',arguname='passwd')
            loginFlag = newUser.isLogin()
            # 加上session看看
            session['logged_in'] = loginFlag
            session['user_id'] = newUser.getUserID()
            session['user_name'] = newUser.getUserName()
            session['user_pcode'] = newUser.getUserPermissions()
            session['login_time'] = newUser.getLoginTime()
        else:
            raise DBDataError(message='no user data found',
                              arguname='')
        # 获取人员权限
        # 需要考虑人员是管理员的情况，管理员标记在人员表上的isadmin
        # isAdminExeSql = db.session.execute(selectUserSql,selectUserPara)
        # isAdminRth = isAdminExeSql.fetchall()
        if getDBPasswdRtn[0][0] == '10':
            # 不是管理员，获取权限列表清单
            current_app.logger.debug('%s is admin'%session.get('user_name'))
            session['isadmin'] = True
        else:
            # 是管理员，获取人员userpermission表所对应的权限
            current_app.logger.debug('%s not admin'%session.get('user_name'))
            session['isadmin'] = False
            userPermListExeSql = db.session.execute(selectPerSql,selectPerPara)
            userPermListRtn = userPermListExeSql.fetchall()
            current_app.logger.debug('%s pervillage list is :'%session.get('user_name'))
            current_app.logger.debug(userPermListRtn)
            selfPermissionList ={}
            for idx,pitem in enumerate(userPermListRtn):
                selfPermissionList[pitem[5]] = 'Y'
            session['permission'] = selfPermissionList
    except DBDataError as err:
        return responseStructures(rstatus=err.code,
                                  rbody={'error_code':err.error_code,
                                         'error_msg':err.message,
                                         'args':err.arguname})
    except Exception as err:
        current_app.logger.error('Unknow Error when analyze post requests para, please chack log file to find detail error message')
        current_app.logger.error(err)
        current_app.logger.error(print_exc())
        return responseStructures(rstatus='521',
                                  rbody={'error_code':1699,
                                         'error_msg':'Unknow Error when analyze post requests para, please chack log file to find detail error message',
                                         'args':''})
    return responseStructures(rstatus='200',
                              rbody={'error_code':2000,
                                     'error_msg':'success'})

@authManagerBP.route('/logoutUser',methods=['POST'])
def logoutUser():
    current_app.logger.debug('=================start log out====================')
    current_app.logger.debug(session.get('logged_in'))
    try:
        if session.get('logged_in'):
            current_app.logger.debug('current user %s will louout'%session.get('user_name'))
            current_app.logger.debug(session.get('user_id'))
            current_app.logger.debug(session.get('user_name'))
            # session['logged_in'] = False
            # 试试看用pop
            session.pop('user_id')
            session.pop('logged_in')
            session.pop('user_name')
            session.pop('user_pcode')
            session.pop('login_time')
            session.pop('permission',None)
            return {'msg':'user logout success!'}
        else:
            return {'msg':'u havent login!'}
    except Exception as err:
        current_app.logger.error(err)
        return {'msg':'error!'}

@authManagerBP.route('/mustLogin',methods=['GET'])
def mustLogin():
    return responseStructures(rstatus='200',
                              rbody={'error_code':'2000',
                                     'error_msg':'u must login system to check this intf',
                                     'args':''})

def wechatMiniPrgLogin():
# 微信小程序登录系统
    pass

def wechatMiniPrgLogout():
# 微信小程序登出系统
    pass

def wechatServerAuth():
# 获取微信公共认证服务
    pass

def userTokenCreater():
# 利用JWT生成用户的Token
# 将用户的一些基础信息也压入Token并加密
    pass

def userTokenSolution():
# 解算用户传递来的Token
    pass

def isLoginCheck(func):
    # 系统登陆校验装饰器
    # 如果未登录返回未授权错误401
    # 当出现小程序时，需要设计一套新的登录校验机制
    # 小程序前端使用token，web前端使用cookie-session，
    # 设想先根据Header中referer或者自定义头进行分离，再根据不同的方法去做逻辑判断
    @wraps(func)
    def loginCheck(*args, **kwargs):
        if session.get('logged_in'):
            current_app.logger.info('user %s is login'%session.get('user_name'))
            return func(*args, **kwargs)
        else:
            current_app.logger.info(session.get('logged_in'))
            return responseStructures(rstatus='401',
                                      rbody={'error_code':1000,
                                             'error_msg':'u must login',
                                             'args':''})
    return loginCheck

def isPermissionCheck(func):
    # 系统权限校验器
    # 设计思路：在登入系统时已将用户所能访问的权限资源清单存储在session内
    # 考虑有系统管理员的情况下，先判断管理员，如果时管理员则全部资源可访问
    # 此处在访问url资源时，根据request.path的访问路径和session['permission']中的json进行比较
    # 如果存在继续执行
    # 如果不存在返回认证错误403
    @wraps(func)
    def permissionCheck(*args, **kwargs):
        if session.get('isadmin'):
            current_app.logger.info('admin user %s allow visit %s'%(session.get('user_name'),request.path))
            current_app.logger.info(request.path)
            return func(*args, **kwargs)
        else:
            if request.path in session.get('permission'):
                current_app.logger.info('user %s allow visit %s'%(session.get('user_name'),request.path))
                current_app.logger.info(request.path)
                return func(*args, **kwargs)
            else:
                current_app.logger.info('user %s not allow visit %s'%(session.get('user_name'),request.path))
                current_app.logger.info(request.path)
                return responseStructures(rstatus='403',
                                          rbody={'error_code':1000,
                                                 'error_msg':'u havent this url permission',
                                                 'args':''})
    return permissionCheck

def isAdminCheck(func):
    # 系统权限校验器
    # 有些权限只需要判断是否是管理员即可，写一个简化的装饰器
    @wraps(func)
    def adminCheck(*args, **kwargs):
        if session.get('isadmin'):
            return func(*args, **kwargs)
        else:
            return responseStructures(rstatus='403',
                                          rbody={'error_code':1000,
                                                 'error_msg':'only admin are allowed to visit this url',
                                                 'args':''})
    return adminCheck