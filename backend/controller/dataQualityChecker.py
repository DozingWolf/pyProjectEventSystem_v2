from loguru import logger

from .backendErrorList import EmptyJsonValue,ErrorJsonData,NoneJsonKey

def isExistCheck(model:list,data:dict):
    # 检查data中是否存在model中指定的数据，如果不存在raise报错
    for checkItem in model:
        if checkItem not in data.keys():
            raise NoneJsonKey(message='miss key column!',keycolumn=checkItem)

def isEmptyCheck(model:list,data:dict):
    # 检查model中指定的key在data中数据是否为空，如果为空raise报错
    for checkItem in model:
        if data[checkItem] == '':
            raise EmptyJsonValue(message='%s is null!'%checkItem,keycolumn=checkItem)