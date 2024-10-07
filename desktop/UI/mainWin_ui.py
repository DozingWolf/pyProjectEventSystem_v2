# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWin.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 30, 81, 16))
        self.lbUname = QLabel(self.centralwidget)
        self.lbUname.setObjectName(u"lbUname")
        self.lbUname.setGeometry(QRect(130, 30, 53, 15))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 80, 53, 15))
        self.lbToken = QLabel(self.centralwidget)
        self.lbToken.setObjectName(u"lbToken")
        self.lbToken.setGeometry(QRect(130, 80, 53, 15))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u9879\u76ee\u4e8b\u4ef6\u7cfb\u7edf", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Uasename:", None))
        self.lbUname.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Token:", None))
        self.lbToken.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

