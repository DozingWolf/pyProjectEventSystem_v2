# 加密解密功能模块
# 供后端Flask与前端Pyside使用
# 需要实现SM国密加解密功能
# 国密研究了下好像在python上面实现有点复杂
# 先用标准的RSA2048和加盐加密吧

from loguru import logger
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

class CryptpError(Exception):
    # 自定义错误类型
    # 用于PKCS1_v1_5解密失败时抛出
    def __init__(self,code, message, type):
        super().__init__(self)
        self.message = message
        self.code = code
        self.type = type
        self.args = (message,)
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message,' ciph type:',self.type])

class SMPassword(object):
    # 国密SM类暂时不实现，等后续有确定的包再说
    def __init__(self):
        pass

class TraditionalPassword(object):
    '''
    类说明：
        传统RSA加解密类
        已定义RSA2048

    使用流程：
        服务侧生成公钥私钥，私钥存储在服务端，公钥分发到客户端
        客户端数据使用公钥进行加密
        传输密文至服务端，服务端使用私钥解密
        
        如果传输的是密码，还需要通过加盐加密之后才能存储至数据库
        密码验证流程为解密RSA2048密码，使用verifyPassword方法进行验证
        密码存储至数据库时，需要使用encryptPassword方法进行加密
        系统变量不存储密码明文
    
    注意事项：
        因为考虑通用性，实例化类后没有初始数据。按照Cryptp.Cipher的方案，请实例化后使用new方法提供私钥。
    '''
    def __init__(self):
        pass

    def __del__(self):
        pass

    def new(self,publicKey):
        # 初始化公钥
        self.__userPublicKey = RSA.importKey(publicKey)

    def generateNewRSAKey(self):
        # 生成RSA公私密钥对
        # 生成的密钥对存储在key文件夹下
        self.__Key = RSA.generate(2048,Random.new().read)
        self.__privateKey = self.__Key.export_key()
        self.__publicKey = self.__Key.publickey().export_key()

        with open('./key/privateKey.pem','wb') as f:
            f.write(self.__privateKey)

        with open('./key/publicKey.pem','wb') as f:
            f.write(self.__publicKey)

        return self.__privateKey,self.__publicKey

    def rsaEncryptStringData(self,plainDataText:str): 
        # 公钥加密
        self.__cipher = PKCS1_v1_5.new(self.__userPublicKey)
        self.__encryptedText = self.__cipher.encrypt(plainDataText.encode('utf-8'))
        return self.__encryptedText
    
    def rsaDecryptStringData(self,encryptedDataText,privateKey):
        # 私钥解密
        self.__userPrivateKey = RSA.importKey(privateKey)
        self.__cipher = PKCS1_v1_5.new(self.__userPrivateKey)
        self.__plainData = self.__cipher.decrypt(encryptedDataText,CryptpError(code='5000',message='私钥解密失败',type='PKCS1_v1_5'))
        return self.__plainData
    
    def encryptPassword(self,passwd):
        # 生成加盐加密密码
        self.__hashPasswd = generate_password_hash(password=passwd,method='scrypt:32768:8:1',salt_length=32)
        logger.debug(passwd)
        logger.debug(self.__hashPasswd)
        return self.__hashPasswd
    
    def verifyPassword(self,userInputPasswd,sysPasswd):
        # 验证加盐密码
        self.__hashPw = userInputPasswd
        self.__plainPw = sysPasswd
        logger.debug(type(userInputPasswd))
        return check_password_hash(pwhash=sysPasswd,password=userInputPasswd)

if __name__ == '__main__':
    # userKeyMaker = TraditionalPassword()
    # userPrivateKey,userPublicKey = userKeyMaker.generateNewRSAKey()
    with open('./key/privateKey.pem','rb') as f:
        userPrivateKey = f.read()
    with open('./key/publicKey.pem','rb') as f:
        userPublicKey = f.read()
    logger.debug('pri key is %r'%userPrivateKey)
    logger.debug('pub key is %r'%userPublicKey)
    userKey = TraditionalPassword()
    userKey.new(publicKey=userPublicKey)
    data = 'admin@123'
    encryptedData = userKey.rsaEncryptStringData(plainDataText=data)
    logger.debug('chiper text is :')
    logger.debug(encryptedData)
    logger.debug(type(encryptedData))
    decryptedData = userKey.rsaDecryptStringData(encryptedDataText=encryptedData,privateKey=userPrivateKey)
    logger.debug(data)
    saltPasswd = userKey.encryptPassword(passwd=data)
    logger.debug(saltPasswd)


    