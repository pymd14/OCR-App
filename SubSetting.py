# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubSetting.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (CardWidget, ComboBox, DoubleSpinBox, LineEdit,
    PrimaryPushButton, PushButton, RadioButton, SubtitleLabel)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1128, 620)
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName(u"CardWidget")
        self.CardWidget.setGeometry(QRect(30, 30, 1030, 60))
        self.CardWidget.setAutoFillBackground(False)
        self.pBtn_Font = PrimaryPushButton(self.CardWidget)
        self.pBtn_Font.setObjectName(u"pBtn_Font")
        self.pBtn_Font.setGeometry(QRect(752, 15, 250, 32))
        self.SubTLabel_Font = SubtitleLabel(self.CardWidget)
        self.SubTLabel_Font.setObjectName(u"SubTLabel_Font")
        self.SubTLabel_Font.setGeometry(QRect(60, 15, 80, 30))
        self.CardWidget_2 = CardWidget(Form)
        self.CardWidget_2.setObjectName(u"CardWidget_2")
        self.CardWidget_2.setGeometry(QRect(30, 110, 1030, 60))
        self.pBtn_Color = PrimaryPushButton(self.CardWidget_2)
        self.pBtn_Color.setObjectName(u"pBtn_Color")
        self.pBtn_Color.setGeometry(QRect(850, 15, 153, 32))
        self.SubTLabel_Color = SubtitleLabel(self.CardWidget_2)
        self.SubTLabel_Color.setObjectName(u"SubTLabel_Color")
        self.SubTLabel_Color.setGeometry(QRect(60, 15, 101, 30))
        self.CardWidget_3 = CardWidget(Form)
        self.CardWidget_3.setObjectName(u"CardWidget_3")
        self.CardWidget_3.setGeometry(QRect(30, 190, 1030, 60))
        self.DSpinBox_acc = DoubleSpinBox(self.CardWidget_3)
        self.DSpinBox_acc.setObjectName(u"DSpinBox_acc")
        self.DSpinBox_acc.setGeometry(QRect(850, 15, 153, 33))
        self.DSpinBox_acc.setDecimals(2)
        self.DSpinBox_acc.setMaximum(1.000000000000000)
        self.DSpinBox_acc.setSingleStep(0.010000000000000)
        self.DSpinBox_acc.setValue(1.000000000000000)
        self.SubTLabel_acc = SubtitleLabel(self.CardWidget_3)
        self.SubTLabel_acc.setObjectName(u"SubTLabel_acc")
        self.SubTLabel_acc.setGeometry(QRect(60, 15, 160, 30))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        self.SubTLabel_acc.setPalette(palette)
        self.CardWidget_4 = CardWidget(Form)
        self.CardWidget_4.setObjectName(u"CardWidget_4")
        self.CardWidget_4.setGeometry(QRect(30, 270, 1030, 60))
        self.ComboBox_OCRS = ComboBox(self.CardWidget_4)
        self.ComboBox_OCRS.setObjectName(u"ComboBox_OCRS")
        self.ComboBox_OCRS.setGeometry(QRect(850, 15, 153, 33))
        self.SubTLabel_OCRS = SubtitleLabel(self.CardWidget_4)
        self.SubTLabel_OCRS.setObjectName(u"SubTLabel_OCRS")
        self.SubTLabel_OCRS.setGeometry(QRect(60, 15, 80, 30))
        self.CardWidget_5 = CardWidget(Form)
        self.CardWidget_5.setObjectName(u"CardWidget_5")
        self.CardWidget_5.setGeometry(QRect(30, 350, 1030, 60))
        self.SubTLabel_Path = SubtitleLabel(self.CardWidget_5)
        self.SubTLabel_Path.setObjectName(u"SubTLabel_Path")
        self.SubTLabel_Path.setGeometry(QRect(60, 17, 101, 30))
        self.LineEdit_Path = LineEdit(self.CardWidget_5)
        self.LineEdit_Path.setObjectName(u"LineEdit_Path")
        self.LineEdit_Path.setGeometry(QRect(329, 16, 671, 33))
        self.CardWidget_6 = CardWidget(Form)
        self.CardWidget_6.setObjectName(u"CardWidget_6")
        self.CardWidget_6.setGeometry(QRect(30, 430, 1030, 60))
        self.SubTLabel_Read = SubtitleLabel(self.CardWidget_6)
        self.SubTLabel_Read.setObjectName(u"SubTLabel_Read")
        self.SubTLabel_Read.setGeometry(QRect(60, 15, 101, 30))
        self.RadioButton_C = RadioButton(self.CardWidget_6)
        self.RadioButton_C.setObjectName(u"RadioButton_C")
        self.RadioButton_C.setGeometry(QRect(820, 20, 70, 24))
        self.RadioButton_C.setChecked(True)
        self.RadioButton_M = RadioButton(self.CardWidget_6)
        self.RadioButton_M.setObjectName(u"RadioButton_M")
        self.RadioButton_M.setGeometry(QRect(935, 20, 70, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pBtn_Font.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u5b57\u4f53", None))
        self.SubTLabel_Font.setText(QCoreApplication.translate("Form", u"\u5b57\u4f53", None))
        self.pBtn_Color.setText("")
        self.SubTLabel_Color.setText(QCoreApplication.translate("Form", u"\u4fee\u8ba2\u989c\u8272", None))
        self.SubTLabel_acc.setText(QCoreApplication.translate("Form", u"\u7f6e\u4fe1\u5ea6\u9608\u503c\u5b9a\u4e49", None))
        self.ComboBox_OCRS.setText("")
        self.SubTLabel_OCRS.setText(QCoreApplication.translate("Form", u"OCR\u6e90", None))
        self.SubTLabel_Path.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.SubTLabel_Read.setText(QCoreApplication.translate("Form", u"\u9605\u8bfb\u4e60\u60ef", None))
        self.RadioButton_C.setText(QCoreApplication.translate("Form", u"\u53e4\u5178", None))
        self.RadioButton_M.setText(QCoreApplication.translate("Form", u"\u73b0\u4ee3", None))
    # retranslateUi

