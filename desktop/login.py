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
from PySide6.QtWidgets import QWidget,QMessageBox,QGraphicsScene
from PySide6.QtCore import Signal,Slot,Qt
from PySide6.QtGui import QMouseEvent,QPixmap

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
        self.__verifyCodeUrl = ''.join(['http://',':'.join(self.parent.getServerInfo()),'/api/v1.0/getVerifyCode'])
        with open('./key/publicKey.pem','rb') as f:
            self.__publicKey = f.read()
        self.leUsercode.setText(self.parent.getLocalRememberUser())
        self.bind()

    def bind(self):
        # 绑定
        self.sendValueToMainWindow.connect(self.parent.lbUname.setText)
        self.sendUserTokenToMain.connect(self.parent.setToken)
        self.pbLogin.clicked.connect(self.sendValue)
        self.pbLogin.clicked.connect(self.postInputDataAndVerify)
        # self.gvVerifyCode.mousePressEvent(self.getVerifyCode) # graphicview控件暂时无法实现点击刷新验证码的效果
        self.pbGetVerifyCode.clicked.connect(self.getVerifyCode)



    def sendValue(self):
        self.sendValueToMainWindow.emit(self.leUsercode.text())
        

    def sendToken(self,token):
        # self.sendUserTokenToMain.emit(self.__tempToken)
        self.sendUserTokenToMain.emit(token)
        logger.info(self.__tempToken)
        self.close()
        self.parent.show()

    def getVerifyCode(self)->None:
        # 获取验证码
        try:
            # 将http访问中的验证码图片展示在graphicsview中
            # 1. 先获取验证码图片的二进制数据
            self.getVerifyReq = get(url=self.__verifyCodeUrl)
            if self.getVerifyReq.status_code!= 200:
                raise ServerError(message='HTTP CODE = %s'%str(self.getVerifyReq.status_code))
            # 
            logger.debug(self.getVerifyReq)
            logger.debug(self.getVerifyReq.cookies)
            self.verifyPix = QPixmap()
            self.verifyPix.loadFromData(self.getVerifyReq.content)
            self.__scene = QGraphicsScene(self)
            self.__scene.clear()
            self.__pixSize = (150,30)
            self.__scene.addPixmap(self.verifyPix)
            # self.__scene.setSceneRect(0,0,self.__pixSize[0],self.__pixSize[1])
            # self.gvVerifyCode.setScene(self.__scene)
            self.gvVerifyCode.fitInView(self.__scene.sceneRect(),Qt.AspectRatioMode.KeepAspectRatio)
            self.gvVerifyCode.show()

        except Exception as e :
            logger.error(format_exc())
            QMessageBox.warning(self,'错误',format_exc(),QMessageBox.StandardButton.Ok)

    def postInputDataAndVerify(self):
        # 登录请求

            # {'code':0,'msg':'success',
            #  'user':'csy',
            #  'auth':[('level1','menu_01'),('level2','menu_02')],
            #  'token':'1234567890'}
        self.__selfChiper = TraditionalPassword()
        self.__selfChiper.new(publicKey=self.__publicKey)
        self.__userName = self.leUsercode.text()
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
            logger.debug(rtnJsonData)
            logger.debug(req)
            # 这里要改成把session传递给主窗口
            
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




