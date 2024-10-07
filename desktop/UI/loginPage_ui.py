# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginPage.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGraphicsView, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_fLoginPage(object):
    def setupUi(self, fLoginPage):
        if not fLoginPage.objectName():
            fLoginPage.setObjectName(u"fLoginPage")
        fLoginPage.resize(400, 408)
        self.verticalLayout = QVBoxLayout(fLoginPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(fLoginPage)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 71, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(fLoginPage)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(60, 30))

        self.horizontalLayout.addWidget(self.label)

        self.leUsername = QLineEdit(fLoginPage)
        self.leUsername.setObjectName(u"leUsername")

        self.horizontalLayout.addWidget(self.leUsername)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.label_2 = QLabel(fLoginPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(60, 30))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lePasswd = QLineEdit(fLoginPage)
        self.lePasswd.setObjectName(u"lePasswd")

        self.horizontalLayout_2.addWidget(self.lePasswd)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.label_3 = QLabel(fLoginPage)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.leVerifyCode = QLineEdit(fLoginPage)
        self.leVerifyCode.setObjectName(u"leVerifyCode")

        self.horizontalLayout_3.addWidget(self.leVerifyCode)

        self.graphicsView = QGraphicsView(fLoginPage)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMaximumSize(QSize(180, 60))

        self.horizontalLayout_3.addWidget(self.graphicsView)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.cbRememberMe = QCheckBox(fLoginPage)
        self.cbRememberMe.setObjectName(u"cbRememberMe")

        self.horizontalLayout_4.addWidget(self.cbRememberMe)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 71, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.pbLogin = QPushButton(fLoginPage)
        self.pbLogin.setObjectName(u"pbLogin")

        self.verticalLayout.addWidget(self.pbLogin)


        self.retranslateUi(fLoginPage)

        QMetaObject.connectSlotsByName(fLoginPage)
    # setupUi

    def retranslateUi(self, fLoginPage):
        fLoginPage.setWindowTitle(QCoreApplication.translate("fLoginPage", u"\u9879\u76ee\u4e8b\u4ef6\u7cfb\u7edf-\u767b\u9646\u7cfb\u7edf", None))
        self.label_4.setText(QCoreApplication.translate("fLoginPage", u"\u9879\u76ee\u4e8b\u4ef6\u7cfb\u7edf", None))
        self.label.setText(QCoreApplication.translate("fLoginPage", u"\u7528\u6237\u540d", None))
        self.label_2.setText(QCoreApplication.translate("fLoginPage", u"\u5bc6   \u7801", None))
        self.label_3.setText(QCoreApplication.translate("fLoginPage", u"\u9a8c\u8bc1\u7801", None))
        self.cbRememberMe.setText(QCoreApplication.translate("fLoginPage", u"\u8bb0\u4f4f\u6211", None))
        self.pbLogin.setText(QCoreApplication.translate("fLoginPage", u"\u767b\u5f55\u7cfb\u7edf", None))
    # retranslateUi

