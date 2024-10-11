from flask import request,session
from flask.blueprints import Blueprint,current_app
from flask.helpers import make_response
from traceback import format_exc
from loguru import logger
from random import sample,randint
from string import ascii_letters,digits
from PIL import Image,ImageFont,ImageDraw,ImageFilter
from io import BytesIO
from time import time

from .dataQualityChecker import isExistCheck,isEmptyCheck
from .backendErrorList import EmptyJsonValue,ErrorJsonData,NoneJsonKey,VerifyCodeError,VerifyTimeoutError

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
        logger.debug('jsonData is :')
        logger.debug(jsonData)
        # 检查json中是否存在empcode,passwd,verifycode三个key
        isExistCheck(model=jsonKeyCheckList,data=jsonData)
        # 检查empcode,passwd,verifycode三个key是否为空
        isEmptyCheck(model=jsonValueNotNullCheckList,data=jsonData)
        # 根据empcode,passwd,verifycode三个key的值分别再数据库与环境中验证
        # 先验证verifycode超时情况
        if session.get('genVerifyTime') is not None:
            if time() - session['genVerifyTime'] > int(current_app.runningConfig['Flask']['verifycode_timeouts']):
                raise VerifyTimeoutError()
        # 再验证verifycode
        if jsonData['verifycode']!= session['verifyCode']:
            raise VerifyCodeError()
        # 校验密码
        getUserPasswdSQL = '''
        select passwd,empname,admin from TMSTUSER where empcode = ?;'''
        cursor = current_app.conn.cursor()
        logger.debug(jsonData['empcode'])
        dbRst = cursor.execute(getUserPasswdSQL,(jsonData['empcode'],))
        userData = dbRst.fetchall()
        logger.debug(bytes(userData[0][0]))

        veriFlag = current_app.sysChiper.verifyPassword(userInputPasswd = current_app.sysChiper.rsaDecryptStringData(encryptedDataText=jsonData['passwd']
                                                                                                                    ,privateKey=current_app.RSA2048PrivateKey),
                                                        sysPasswd = userData[0][0])
        logger.debug(veriFlag)
        
        # 通过全部校验后，将数据保存到session中
        session['logged_in'] = True
        session['currentUser'] = jsonData['empcode']
        rtnMsg = {'code':2000,'msg':'login success'}
        return make_response(rtnMsg)

    except VerifyTimeoutError as e:
        rtnMsg = {'code':e.code,'msg':e.message}
        return make_response(rtnMsg)
    except VerifyCodeError as e:
        rtnMsg = {'code':e.code,'msg':e.message}
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

@loginManagerBP.route('/logout',methods=['POST'])
def logout():
    if session.get('logged_in') is True:
        session['logged_in'] = False
        session['currentUser'] = None
        rtnMsg = {'code':2000,'msg':'logout success'}
    else:
        rtnMsg = {'code':2000,'msg':'already logged out'}
    return make_response(rtnMsg)

@loginManagerBP.route('/getVerifyCode',methods=['GET'])
def getVerifyCode():
    # 生成验证码
    # 生成随机字符串
    verifyString = ''.join(sample(ascii_letters + digits, 4))
    logger.debug(verifyString)
    # 定义图片大小
    width, height = 130, 50
    # 生成图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 定义字体
    verifyFont = ImageFont.truetype('./static/AlibabaSans-Medium.otf', 50)
    # 绘制对象
    draw = ImageDraw.Draw(im)
    for item in range(4):
        draw.text((5 + randint(-3, 3) + 30 * item, -15 + randint(-3, 3)),
                  text=verifyString[item],
                  fill=(randint(32, 127), randint(32, 127), randint(32, 127)),
                  font=verifyFont)
    # 绘制干扰线
    for i in range(randint(3, 5)):
        x1 = randint(0, width/2)
        y1 = randint(0, height/2)
        x2 = randint(0, width)
        y2 = randint(height/2, height)
        draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0), width=1)
    # 形成传输对象
    buf = BytesIO()
    im.save(buf,'png',quality=90)
    bufString = buf.getvalue()
    # 反馈前端验证码图片
    responseStruct = make_response(bufString)
    responseStruct.headers['Content-Type'] = 'image/png'
    # 保存session中的验证码
    session['verifyCode'] = verifyString
    # 保存session的生成时间，用于过期验证
    session['genVerifyTime'] =  time()
    return responseStruct