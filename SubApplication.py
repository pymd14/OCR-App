# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubApplication.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGraphicsView,
    QHeaderView, QSizePolicy, QWidget)

from qfluentwidgets import (CardWidget, CheckBox, ComboBox, PixmapLabel,
    PlainTextEdit, PrimaryPushButton, PrimaryToolButton, PushButton,
    StrongBodyLabel, SubtitleLabel, TableView, ToolButton,
    TransparentToolButton)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(1266, 860)
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName(u"CardWidget")
        self.CardWidget.setGeometry(QRect(20, 10, 380, 485))
        self.CardWidget.setAutoFillBackground(False)
        self.graphicsView = QGraphicsView(self.CardWidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(10, 48, 360, 430))
        self.pBtnimport = PrimaryPushButton(self.CardWidget)
        self.pBtnimport.setObjectName(u"pBtnimport")
        self.pBtnimport.setGeometry(QRect(10, 10, 315, 32))
        self.PTBtnOCR = PrimaryToolButton(self.CardWidget)
        self.PTBtnOCR.setObjectName(u"PTBtnOCR")
        self.PTBtnOCR.setGeometry(QRect(332, 10, 38, 32))
        self.Piximport = PixmapLabel(self.CardWidget)
        self.Piximport.setObjectName(u"Piximport")
        self.Piximport.setGeometry(QRect(10, 48, 360, 430))
        self.CardWidget_2 = CardWidget(Form)
        self.CardWidget_2.setObjectName(u"CardWidget_2")
        self.CardWidget_2.setGeometry(QRect(410, 10, 830, 485))
        self.CardWidget_2.setAutoFillBackground(False)
        self.graViewLocation = QGraphicsView(self.CardWidget_2)
        self.graViewLocation.setObjectName(u"graViewLocation")
        self.graViewLocation.setGeometry(QRect(20, 48, 390, 390))
        self.graViewrRevision = QGraphicsView(self.CardWidget_2)
        self.graViewrRevision.setObjectName(u"graViewrRevision")
        self.graViewrRevision.setGeometry(QRect(430, 48, 390, 390))
        self.PlainTextRevision = PlainTextEdit(self.CardWidget_2)
        self.PlainTextRevision.setObjectName(u"PlainTextRevision")
        self.PlainTextRevision.setGeometry(QRect(430, 48, 390, 390))
        self.PlainTextRevision.setFrameShape(QFrame.StyledPanel)
        self.PlainTextRevision.setFrameShadow(QFrame.Sunken)
        self.PlainTextRevision.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.PlainTextRevision.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SubLabel = SubtitleLabel(self.CardWidget_2)
        self.SubLabel.setObjectName(u"SubLabel")
        self.SubLabel.setGeometry(QRect(18, 9, 91, 32))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(14)
        font.setBold(True)
        self.SubLabel.setFont(font)
        self.ComboBox = ComboBox(self.CardWidget_2)
        self.ComboBox.setObjectName(u"ComboBox")
        self.ComboBox.setGeometry(QRect(119, 10, 571, 32))
        self.CheckBox = CheckBox(self.CardWidget_2)
        self.CheckBox.setObjectName(u"CheckBox")
        self.CheckBox.setGeometry(QRect(710, 12, 92, 30))
        self.CheckBox.setCheckable(False)
        self.pBtnSave = PrimaryPushButton(self.CardWidget_2)
        self.pBtnSave.setObjectName(u"pBtnSave")
        self.pBtnSave.setGeometry(QRect(50, 444, 330, 32))
        self.pBtnCancle = PrimaryPushButton(self.CardWidget_2)
        self.pBtnCancle.setObjectName(u"pBtnCancle")
        self.pBtnCancle.setGeometry(QRect(460, 444, 330, 32))
        self.PixLocation = PixmapLabel(self.CardWidget_2)
        self.PixLocation.setObjectName(u"PixLocation")
        self.PixLocation.setGeometry(QRect(20, 48, 390, 390))
        self.CardWidget_3 = CardWidget(Form)
        self.CardWidget_3.setObjectName(u"CardWidget_3")
        self.CardWidget_3.setGeometry(QRect(20, 500, 1170, 341))
        self.CardWidget_3.setAutoFillBackground(False)
        self.TableView = TableView(self.CardWidget_3)
        self.TableView.setObjectName(u"TableView")
        self.TableView.setGeometry(QRect(10, 26, 1150, 310))
        font1 = QFont()
        font1.setPointSize(10)
        self.TableView.setFont(font1)
        self.TableView.setMidLineWidth(1)
        self.TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.TableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableView.setShowGrid(True)
        self.TableView.verticalHeader().setVisible(False)
        self.StrongBodyLabel = StrongBodyLabel(self.CardWidget_3)
        self.StrongBodyLabel.setObjectName(u"StrongBodyLabel")
        self.StrongBodyLabel.setGeometry(QRect(20, 4, 171, 19))
        self.pBtnBinding = PrimaryPushButton(Form)
        self.pBtnBinding.setObjectName(u"pBtnBinding")
        self.pBtnBinding.setGeometry(QRect(1196, 500, 45, 341))
        font2 = QFont()
        font2.setFamilies([u"\u96b6\u4e66"])
        font2.setPointSize(16)
        font2.setBold(False)
        self.pBtnBinding.setFont(font2)
        self.PixBinding = TransparentToolButton(Form)
        self.PixBinding.setObjectName(u"PixBinding")
        self.PixBinding.setEnabled(False)
        self.PixBinding.setGeometry(QRect(1198, 548, 40, 40))
        self.PixBinding.setIconSize(QSize(20, 20))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pBtnimport.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u56fe\u7247", None))
        self.SubLabel.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u9009\u62e9", None))
        self.ComboBox.setText(QCoreApplication.translate("Form", u"---\u8bf7\u9009\u62e9\u76ee\u6807\u533a\u57df---", None))
        self.CheckBox.setText(QCoreApplication.translate("Form", u"\u6821\u9a8c\u72b6\u6001", None))
        self.pBtnSave.setText(QCoreApplication.translate("Form", u"\u6821\u9a8c\u5b8c\u6210", None))
        self.pBtnCancle.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
        self.StrongBodyLabel.setText(QCoreApplication.translate("Form", u"\u68c0\u6d4b\u7ed3\u679c\u4e0e\u4f4d\u7f6e\u4fe1\u606f", None))
        self.pBtnBinding.setText(QCoreApplication.translate("Form", u"\n"
"\u88c5\n"
"\n"
"\u8ba2\n"
"\n"
"\u6210\n"
"\n"
"\u518c", None))
    # retranslateUi

