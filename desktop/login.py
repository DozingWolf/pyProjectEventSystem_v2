# import UI
from UI.loginPage_ui import Ui_fLoginPage 
# import business logic
from errorlist import ServerError
from controller.dataEncrypt import TraditionalPassword 
# import system package
from loguru import logger
from requests import post,get
from json import dumps,loads
from traceback import format_exc
# import pyside
from PySide6.QtWidgets import QWidget,QMessageBox
from PySide6.QtCore import Signal,Slot

class LoginPage(QWidget,Ui_fLoginPage):
    sendValueToMainWindow = Signal(str)
    sendUserTokenToMain = Signal(str)
    sendRememberInfo = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.__tempToken = ''
        self.parent = parent
        self.setupUi(self)
        self.__loginUrl = ''.join(['http://',':'.join(self.parent.getServerInfo()),'/api/v1.0/login'])
        self.__verifyCodeUrl = ''.join([':'.join(self.parent.getServerInfo()),'/api/v1.0/getVerifyCode'])
        with open('./key/publicKey.pem','rb') as f:
            self.__publicKey = f.read()
        self.leUsername.setText(self.parent.getLocalRememberUser())
        self.bind()

    def bind(self):
        # 绑定
        self.sendValueToMainWindow.connect(self.parent.lbUname.setText)
        self.sendUserTokenToMain.connect(self.parent.setToken)
        self.pbLogin.clicked.connect(self.sendValue)
        self.pbLogin.clicked.connect(self.postInputDataAndVerify)

    def sendValue(self):
        self.sendValueToMainWindow.emit(self.leUsername.text())
        

    def sendToken(self,token):
        # self.sendUserTokenToMain.emit(self.__tempToken)
        self.sendUserTokenToMain.emit(token)
        logger.info(self.__tempToken)
        self.close()
        self.parent.show()


    def getVerifyCode(self):
        # 获取验证码
        req = get(url=self.__verifyCodeUrl)

    def postInputDataAndVerify(self):
        # 登录请求

            # {'code':0,'msg':'success',
            #  'user':'csy',
            #  'auth':[('level1','menu_01'),('level2','menu_02')],
            #  'token':'1234567890'}
        self.__selfChiper = TraditionalPassword()
        self.__selfChiper.new(publicKey=self.__publicKey)
        self.__userName = self.leUsername.text()
        self.__passWord = self.__selfChiper.rsaEncryptStringData(plainDataText=self.lePasswd.text())
        self.__verifyCode = self.leVerifyCode.text()
        self.__loginQueryHeader = {'Content-Type':'application/json'}
        self.__loginQueryBody = {'empcode':self.__userName,
                                 'passwd':str(self.__passWord),
                                 'verifycode':self.__verifyCode}
        try:
            req = post(url=self.__loginUrl,
                       headers=self.__loginQueryHeader,
                       data=dumps(self.__loginQueryBody))
            if req.status_code != 200:
                raise ServerError(message='HTTP CODE = %s'%str(req.status_code))
            rtnJsonData = req.json()
            logger.info(rtnJsonData)
            logger.debug(req)
            # 这里要改成把session传递给主窗口
            # self.__tempToken = rtnJsonData['token']
            # logger.info(type(rtnJsonData))
            # self.sendToken(self.__tempToken)
        except ServerError as e:
            logger.error(format_exc())
            QMessageBox.warning(self,'错误','HTTP接口错误,HTTP CODE %s'%str(req.status_code),QMessageBox.StandardButton.Ok)
        except Exception as e:
            logger.error(format_exc())
            QMessageBox.warning(self,'错误',format_exc(),QMessageBox.StandardButton.Ok)

    def loginSystem(self):
        # 登录系统
        # 1. 先通过postInputDataAndVerify函数获取当前界面输入的用户名密码和验证码，通过接口进行验证
        # 2. 验证成功后，获取token，通过信号发送给主界面
        # 3. 关闭当前界面，显示主界面
        pass

    def saveRememberUser(self):
        # 保存记住用户
        if self.cbRememberMe.isChecked():
            pass




