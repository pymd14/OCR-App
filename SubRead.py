# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubRead.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QHeaderView, QSizePolicy, QTreeWidgetItem, QWidget)

from qfluentwidgets import (CardWidget, LineEdit, PlainTextEdit, SearchLineEdit,
    TreeWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(1266, 860)
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName(u"CardWidget")
        self.CardWidget.setGeometry(QRect(10, 10, 251, 831))
        self.CardWidget.setAutoFillBackground(False)
        self.SearchLineEdit = SearchLineEdit(self.CardWidget)
        self.SearchLineEdit.setObjectName(u"SearchLineEdit")
        self.SearchLineEdit.setGeometry(QRect(6, 10, 240, 33))
        self.TreeWidBook = TreeWidget(self.CardWidget)
        self.TreeWidBook.setObjectName(u"TreeWidBook")
        self.TreeWidBook.setGeometry(QRect(6, 50, 240, 771))
        font = QFont()
        font.setPointSize(10)
        self.TreeWidBook.setFont(font)
        self.TreeWidBook.setFrameShape(QFrame.NoFrame)
        self.TreeWidBook.setFrameShadow(QFrame.Plain)
        self.TreeWidBook.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.TreeWidBook.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.TreeWidBook.setSortingEnabled(False)
        self.TreeWidBook.setHeaderHidden(False)
        self.TreeWidBook.header().setVisible(True)
        self.TreeWidBook.header().setCascadingSectionResizes(False)
        self.TreeWidBook.header().setMinimumSectionSize(30)
        self.TreeWidBook.header().setProperty("showSortIndicator", False)
        self.TreeWidBook.header().setStretchLastSection(True)
        self.CardWidget_2 = CardWidget(Form)
        self.CardWidget_2.setObjectName(u"CardWidget_2")
        self.CardWidget_2.setGeometry(QRect(269, 10, 980, 831))
        self.CardWidget_2.setAutoFillBackground(False)
        self.graViewText = QGraphicsView(self.CardWidget_2)
        self.graViewText.setObjectName(u"graViewText")
        self.graViewText.setGeometry(QRect(430, 10, 540, 810))
        self.PlainText = PlainTextEdit(self.CardWidget_2)
        self.PlainText.setObjectName(u"PlainText")
        self.PlainText.setGeometry(QRect(430, 10, 540, 810))
        self.PlainText.setFrameShape(QFrame.StyledPanel)
        self.PlainText.setFrameShadow(QFrame.Sunken)
        self.PlainText.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.PlainText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frame = QFrame(self.CardWidget_2)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 150, 410, 410))
        self.frame.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(0, 170, 255);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"border: 0px solid red;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtreewidgetitem = self.TreeWidBook.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u6211\u7684\u85cf\u4e66", None));
    # retranslateUi

