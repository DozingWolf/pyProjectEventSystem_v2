# import UI
from UI.mainWin_ui import Ui_MainWindow
# import business logic
from errorlist import EmpytParameterError
from login import LoginPage 
# import system package
from loguru import logger
from configparser import ConfigParser
from traceback import format_exc
# import pyside
from PySide6.QtWidgets import QWidget,QApplication,QMainWindow,QErrorMessage
from PySide6.QtCore import Signal,Slot

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.__currentUserToken = ''
        try:
            self.__params = ConfigParser()
            self.__params.read('./conf/conf.ini')
            if len(self.__params.sections()) == 0:
                raise EmpytParameterError(message='未读取到配置文件信息')
            self.Server = self.__params['Server']['server']
            self.Port = self.__params['Server']['port']
            if self.Server == '':
                raise EmpytParameterError(message='配置文件中缺少服务器IP信息')
            if self.Port == '':
                raise EmpytParameterError(message='配置文件中缺少服务器端口信息')
            logger.info('IP %s ,Port %s'%(self.__params['Server']['server'],
                                          str(self.__params['Server']['port'])))
            logger.info('配置读取成功')
            self.setupUi(self)
            self.lbUname.setText('')
            self.bind()

        except EmpytParameterError as e:
            logger.error(format_exc())
        except Exception as e:
            logger.error(format_exc())

    def bind(self):
        self.loginPage = LoginPage(self)
        self.loginPage.show()

    def getServerInfo(self):
        return self.Server,self.Port
    
    def getLocalRememberUser(self):
        if self.__params['Desktop']['uname'] == '':
            return None
        else:
            return self.__params['Desktop']['uname']
        
    def saveUserParam(self,user):
        self.__params['Desktop']['uname'] = user
        with open('./desktop/conf/conf.ini','w') as f:
            self.__params.write(f)

    def setToken(self,token):
        self.__currentUserToken = token
        self.lbToken.setText(self.__currentUserToken)

    def getCurrentUserToken(self):
        return self.__currentUserToken

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    # window.show()
    app.exec()


