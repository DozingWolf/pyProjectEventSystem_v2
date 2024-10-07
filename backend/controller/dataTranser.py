from flask import current_app
from datetime import datetime
from time import mktime,strptime
from base64 import urlsafe_b64decode,urlsafe_b64encode
from loguru import logger
from datetime import datetime

def dbDataTransJson(inputdata:list,title:list):
    # sqlalchemy数据代理转dict,反馈给业务服务一个dict结构的数据，转json由业务代码进行
    # 不直接转json的原因是外部还需要拼装状态码、说明等信息，多次编码转换不优雅
    # 20220407 输入增加标题行，输出变更为一个包含数据dict的list
    # 输入得title元素数量需要和inputdata的列数量一致
    # 但需要兼容结果集是空的情况，所以将判断放在拆解循环内进行
    titleCount = len(title)
    logger.debug(inputdata)
    countRowNum = len(inputdata)
    rtnData = {'rownum':-1,'rowdata':[]}
    rtnData['rownum'] = countRowNum
    if countRowNum >= 1:
        inputColCount = len(inputdata[0])
        if titleCount == inputColCount:
            for rid,row in enumerate(inputdata):
                colDict = {}
                for cid,col in enumerate(row):
                    if isinstance(col,datetime):
                        # 当数据出现datetime类型时，需要处理一下
                        col = str(col)
                    colDict[title[cid]] = col
                rtnData['rowdata'].append([rid,colDict])
        else:
            raise Exception(message='input arguments error,count title not equal count column',
                                     arguname='inputdata')
    else:
        pass
    logger.debug(rtnData)
    return rtnData

def dateStrTransTimestamp(input:str):
    # 将字符串的时间转换为timestamp类型
    current_app.logger.debug('input data is: %s'%input)
    timeFormat = '%Y-%m-%d %H:%M:%S'
    timeArray = strptime(input,timeFormat)
    rtnTimestamp = mktime(timeArray)
    rtnmsg = type(rtnTimestamp)
    logger.debug('type is :%s'%rtnmsg)
    return rtnTimestamp

def b64TransString(input:str):
    # 将base64转换为password
    b64bytes = bytes(input,encoding='utf8')
    # current_app.logger.debug('password is : %s'%b64bytes)
    passwd = urlsafe_b64decode(b64bytes).decode('utf-8')
    logger.debug('str password is : %s'%passwd)
    return passwd

def strTransB64(input:str):
    # 将字符串转换为base64
    bytesStr = bytes(input,encoding='utf8')
    encryptStr = urlsafe_b64encode(bytesStr).decode('utf-8')
    logger.debug('encrypt string is %s'%encryptStr)
    return encryptStr

def getCurrentTimeFormatString():
    # 获取当前时间字符串
    currentTime = datetime.now()
    currentTimeStr = currentTime.strftime('%Y-%m-%d %H:%M:%S')
    return currentTimeStr