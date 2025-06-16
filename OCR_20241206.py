# coding:utf-8
import sys
import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List

import cv2
import numpy as np
import shortuuid
import shutil
from PySide6.QtCore import Qt, QObject, QUrl, Signal, QTimer, QFileSystemWatcher, QRectF
from PySide6.QtGui import QIcon, QDesktopServices, QPixmap, QStandardItemModel, QStandardItem, QColor, QBrush, QFont, QPainter, QFontMetrics, QPen
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QLabel, QScrollArea,
                            QFileDialog, QColorDialog, QFontDialog)
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow, NavigationAvatarWidget, qrouter, PlainTextEdit, SubtitleLabel, setFont, CheckBox, TreeView,
                            ElevatedCardWidget, StrongBodyLabel, PillPushButton, SmoothScrollArea, TeachingTip, TeachingTipTailPosition, InfoBarIcon, InfoBar, InfoBarPosition, FlowLayout)
from qfluentwidgets import FluentIcon as FIF

from SubApplication import Ui_Form as AppUi
from SubBookShelf import Ui_Form as BookShelfUi
from SubRead import Ui_Form as ReadUi
from SubSetting import Ui_Form as SetUi

import pyqtgraph as pg
from signal_bus import signalBus


@dataclass
class InfoBarMsgModel:
    type: str = field(default="success")
    title: str = field(default="")
    content: str = field(default="")
    orient: Qt = field(default=Qt.Horizontal)
    isClosable: bool = field(default=False)
    duration: int = field(default=1000)
    position: InfoBarPosition = field(default=InfoBarPosition.TOP)


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        # 全局infoBar信号
        signalBus.showInfoBar.connect(self.showInfoBar)
        # create sub interface
        self.homeInterface = Widget('Home Interface', self)
        self.appInterface = SubApplication('Sub Application', self)
        self.bookshelfInterface = SubBookShelf('Sub BookShelf', self)
        self.readInterface = SubRead('Sub Read', self)

        self.settingInterface = SubSetting('Sub Setting', self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # HOME_FILL表示点击后变成另一个图标
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        self.addSubInterface(self.bookshelfInterface, FIF.BOOK_SHELF, '书架')
        self.addSubInterface(self.readInterface, FIF.QUICK_NOTE, '阅读')

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1350, 910)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('OCR-Title--PyQt-Fluent-Widgets')
        # 获取用户屏幕尺寸
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox(
            'Messagetitle',
            'MessageContent',
            self
        )
        w.yesButton.setText('确定')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))

    def showInfoBar(self, infoBarMsgModel: InfoBarMsgModel):
        infoBarFuc: Callable = None
        if infoBarMsgModel.type == "error":
            infoBarFuc = InfoBar.error
        elif infoBarMsgModel.type == "success":
            infoBarFuc = InfoBar.success

        infoBarFuc(title=infoBarMsgModel.title, content=infoBarMsgModel.content,
                   orient=infoBarMsgModel.orient, isClosable=infoBarMsgModel.isClosable,
                   duration=infoBarMsgModel.duration, position=infoBarMsgModel.position, parent=self)


# 2024-12-06 新写个类，用于加载settings的json文件，并将设置发射出去。
class SettingsManager(QObject):
    # 定义一个信号，发射json键值对
    settingVar = Signal(dict)

    def __init__(self, settings_file, parent=None):
        super().__init__(parent)
        self.settings_file = settings_file

    def loadSettings(self):
        # 从 JSON 文件中读取设置，并发射出去
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as json_file:
                    settings = json.load(json_file)
                    # 发射信号，将设置作为字典传递
                    self.settingVar.emit(settings)
            else:
                print(f"Settings file '{self.settings_file}' does not exist.")
        except Exception as e:
            print(f"Error loading settings: {e}")

# 定义ui类，目的是为了在Window类中实例化并部署到“应用”页面
class SubApplication(AppUi, QWidget):
    # 定义信号
    update = Signal(bool)

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.PTBtnOCR.setIcon(FIF.SYNC)
        self.PixBinding.setIcon(FIF.BOOK_SHELF)
        self.pBtnimport.clicked.connect(self.open_img)
        self.PTBtnOCR.clicked.connect(self.show_result)
        self.pBtnSave.clicked.connect(self.save)
        self.pBtnCancle.clicked.connect(self.cancle)
        self.pBtnBinding.clicked.connect(self.binding)
        self.CheckBox.setChecked(False)
        self.setObjectName(text.replace(' ', '-'))
        self.file_name = None
        self.combo_dict = []

        self.update.connect(self.update_checkbox)

        if self.ComboBox.currentIndex() < len(self.combo_dict):
            self.ComboBox.currentIndexChanged.connect(self.choose_combobox)
        else:
            self.ComboBox.setText("---请选择目标区域---")

        # 源目录和目标目录
        self.crop_dir = '../OCR/history_img'
        self.binding_dir = '../OCR/binding'

        # 2024-12-06 在SubApplication中实例化SettingsManager
        self.settings_manager = SettingsManager('settings')
        # 连接信号
        self.settings_manager.settingVar.connect(self.receivedAppSettings)
        # 从文件加载设置并发射信号
        self.settings_manager.loadSettings()
    # 接收设置并实例化变量
    def receivedAppSettings(self, settings):
        # 信号接收到settings并逐个实例化成变量，供SubApplication调用
        for key, value in settings.items():
            setattr(self, key, value)
        self.appli_font_family = self.font_family
        self.appli_font_size = self.font_size
        self.appli_confidence = self.confidence
        self.appli_color = self.color
        self.appli_ocrs = self.ocrs
        self.appli_status_C = self.status_C
        self.appli_status_M = self.status_M
        self.appli_path = self.path

    def open_img(self):
        # 初始化，确保打开图片时都是空白状态
        self.combo_dict.clear()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择需要导入的图片", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)

        if file_name:
            pixmap = QPixmap(file_name)
            # 自适应格式使图片不会过分失真
            scaled_pixmap = pixmap.scaled(360, 430)
            self.Piximport.setPixmap(scaled_pixmap)
            self.Piximport.setFixedSize(360, 430)
            self.file_name = file_name
        else:
            return None

    def show_result(self):
        # 识别单张图片，将识别结果输出到PlainTextRevision
        from paddleocr import PaddleOCR, draw_ocr
        # import os
        os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
        img_path = self.file_name
        # 初始化 PaddleOCR 模型，只需运行一次以下载并加载模型到内存中
        ocr_txt = PaddleOCR(use_angle_cls=True, lang="ch",device='cpu')
        # 使用 PaddleOCR 模型进行文字识别，识别结果result_t为list+turple的2维数组
        result_t = ocr_txt.ocr(img_path, cls=True)
        # 把result_t转换成3列数组
        new = [((item[0]), (item[1][0]), (item[1][1])) for item in result_t[0]]
        row = len(new)
        column = len(new[0]) if new[0] else 0
        # 将识别结果拼接成一个字符串
        text_result = ""
        for i in range(len(result_t)):
            res = result_t[i]
            for line in res:
                text_result += line[1][0] + "\n"
        self.PlainTextRevision.setPlainText(text_result)
        font = QFont(self.appli_font_family, self.appli_font_size)
        self.PlainTextRevision.setFont(font)
        # self.graViewrevision.setFixedSize(390, 390)

        # 将识别结果集显示到TableView中
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['序号', '坐标', '结果', '置信度', '校验状态'])
        self.TableView.setBorderRadius(8)
        # 填充单元格数据
        for i in range(row):
            serial = QStandardItem(str(i + 1))  # 序号从 1 开始
            model.setItem(i, 0, serial)
            for j in range(column):
                item = QStandardItem(str(new[i][j]))
                model.setItem(i, j + 1, item)

            confidence = new[i][2]
            if confidence < self.appli_confidence:
                # color = QColor(self.color)
                # 将置信度小于0.95的单元格设置为红色
                item.setForeground(QBrush(QColor(self.color)))

                # 增加复选框
            checkbox_item = QStandardItem()
            checkbox_item.setCheckable(True)  # 复选框前缀图形框可见
            checkbox_item.setText('未校验')
            checkbox_item.setEnabled(False)
            model.setItem(i, column + 1, checkbox_item)
        self.TableView.setModel(model)
        # 调整列宽以适应内容
        self.TableView.resizeColumnsToContents()
        self.TableView.setColumnWidth(4, 120)  # 第五列非数组单元格，手动调整第5列宽度
        self.TableView.show()
        # 将识别结果输出到ComboBox中
        combolist = [((item[0])) for item in new]
        # 每次填充前先清空ComboBox
        self.ComboBox.items.clear()
        for i in range(len(combolist)):
            self.ComboBox.addItem('序号' + str(i + 1) + '    ' + str(combolist[i]))

        # 将识别结果按det坐标切割并保存，用于与ComboBox匹配显示
        # img = cv2.imread(self.file_name)
        img = cv2.imdecode(np.fromfile(self.file_name, dtype=np.uint8), -1)
        # combo_dict = []
        for i, line in enumerate(new):
            # line[0] 包含坐标信息
            box = line[0]  # 获取坐标点
            # box 是一个四个点的列表，按顺序为 [左上, 右上, 右下, 左下]
            points = box[0]  # 提取左上角坐标 (x1, y1)
            x1, y1 = int(points[0]), int(points[1])  # 转换为整数
            points = box[2]  # 提取右下角坐标 (x2, y2)
            x2, y2 = int(points[0]), int(points[1])  # 转换为整数
            # 切割图像
            crop_img = img[y1:y2, x1:x2]
            # 构造保存路径
            crop_img_dir = f'history_img/{os.path.splitext(os.path.basename(self.file_name))[0]}'  # history_img
            crop_img_serial = f'{crop_img_dir}/cropped_serial_{i + 1}.jpg'
            # 检查目录是否存在，如果不存在则创建
            os.makedirs(crop_img_dir, exist_ok=True)
            cv2.imwrite(crop_img_serial, crop_img)

            self.combo_dict.append(crop_img_serial)

        # self.combo_dict = combo_dict

    def choose_combobox(self):
        current_index = self.ComboBox.currentIndex()

        if 0 <= current_index < len(self.combo_dict):
            # 根据选择的索引获取对应的图片路径
            selected_image_path = self.combo_dict[current_index]
            pixmap = QPixmap(selected_image_path)
            pixw = pixmap.width()
            pixh = pixmap.height()
            if pixw > 390 or pixh > 390:
                # # 选择较小的缩放比例并计算
                scale = min(390 / pixw, 390 / pixh)
                new_pixmap = pixmap.scaled(pixw * scale, pixh * scale, Qt.KeepAspectRatio)
                self.PixLocation.setPixmap(new_pixmap)
            else:
                self.PixLocation.setPixmap(pixmap)
            # self.PixLocation.setScaledContents(True)

            model, current_index = self.get_model()
            if current_index >= 0:
                value = model.data(model.index(current_index, 4))
                self.CheckBox.setText(value)
                if value == '已校验':
                    self.CheckBox.setCheckable(True)
                    self.CheckBox.setChecked(True)
                else:
                    self.CheckBox.setCheckable(True)
                    self.CheckBox.setChecked(False)

    def save(self):
        model, current_index = self.get_model()
        if current_index >= 0:
            row_index = model.index(current_index, 4)
            model.setData(row_index, "已校验")
            checkbox_item = model.item(current_index, 4)  # 获取复选框项
            if checkbox_item is not None:
                checkbox_item.setCheckState(Qt.Checked)
                self.update.emit(True)
        else:
            pass

    def cancle(self):
        model, current_index = self.get_model()
        if current_index >= 0:
            row_index = model.index(current_index, 4)
            model.setData(row_index, "未校验")
            checkbox_item = model.item(current_index, 4)  # 获取复选框项
            if checkbox_item is not None:
                checkbox_item.setCheckState(Qt.Unchecked)
                self.update.emit(True)
        else:
            pass

    def get_model(self):
        model = self.TableView.model()
        current_index = self.ComboBox.currentIndex()
        return model, current_index

    def update_checkbox(self):
        model, current_index = self.get_model()
        if current_index >= 0:
            value = model.data(model.index(current_index, 4))
            self.CheckBox.setText(value)
        if value == '已校验':
            self.CheckBox.setChecked(True)
        else:
            self.CheckBox.setChecked(False)

    def binding(self):
        text_result = self.PlainTextRevision.toPlainText()
        # filename = os.path.splitext(os.path.basename(self.file_name))[0]
        # 保存图片
        if not self.combo_dict:
            InfoBar.error(
                title='无效操作',
                content='请先识别图片',
                orient=Qt.Horizontal,
                # orient=Qt.Vertical,
                isClosable=False,
                position=InfoBarPosition.BOTTOM,
                duration=3000,  # -1不会自动消失
                parent=self
            )
        else:
            model = self.TableView.model()
            for row in range(model.rowCount()):
                # 获取第5列校验状态
                check_status = model.item(row, 4).text()
                if check_status.strip() == "未校验":
                    warning_message = f"第{row + 1}行（{check_status}），请复核。"
                    InfoBar.warning(
                        title='校验未完成',
                        content=warning_message,
                        orient=Qt.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.BOTTOM,
                        duration=3000,  # -1不会自动消失
                        parent=self
                    )
                    return

            options = QFileDialog.Options()
            binding_path, _ = QFileDialog.getSaveFileName(self, "装订文件", self.binding_dir, "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)
            if not os.path.exists(os.path.dirname(binding_path)):
                os.makedirs(os.path.dirname(binding_path))
            try:
                if hasattr(self, 'file_name') and self.file_name:
                    binding_img_path = binding_path.rsplit('.', 1)[0] + '.png'
                    shutil.copy(self.file_name, binding_img_path)
            except Exception as e:
                InfoBar.error(
                    title='文件已被装订过',
                    content=str(e),
                    orient=Qt.Horizontal,
                    # orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,  # -1不会自动消失
                    parent=self
                )

            """
            filename = os.path.splitext(os.path.basename(self.file_name))[0]
            # 构造图片名
            binding_pic = os.path.join(self.binding_dir, filename)
            # 检查目标目录是否存在，如果不存在则创建
            if not os.path.exists(binding_pic):
                os.makedirs(binding_pic)
            try:
                shutil.copy(self.file_name, binding_pic)
            except Exception as e:
                InfoBar.error(
                    title='文件已被装订过',
                    content=str(e),
                    orient=Qt.Horizontal,
                    # orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=3000,  # -1不会自动消失
                    parent=self
                )
                """
            # filename = os.path.splitext(os.path.basename(self.file_name))[0]
            # 构造文件名
            # txt_name = f"{filename}.txt"
            # 保存文本
            if text_result.strip():  # 检查文本是否为空
                try:
                    if hasattr(self, 'PlainTextRevision') and isinstance(self.PlainTextRevision, PlainTextEdit):
                        text = self.PlainTextRevision.toPlainText()
                        binding_txt_path = binding_path.rsplit('.', 1)[0] + '.txt'  # 给文本文件加上扩展名
                        with open(binding_txt_path, 'w', encoding='utf-8') as txt:
                            txt.write(text)
                        InfoBar.success(
                            title='装订成功',
                            content='文件已保存至' + str(os.path.dirname(binding_path)),
                            orient=Qt.Horizontal,
                            # orient=Qt.Vertical,
                            isClosable=False,
                            position=InfoBarPosition.BOTTOM,
                            duration=3000,  # -1不会自动消失
                            parent=self
                        )
                    """
                    binding_txt = os.path.join(self.binding_dir, filename)
                    if not os.path.exists(binding_txt):  # 如果目录不存在，则创建
                        os.makedirs(binding_txt)
                    txt_path = os.path.join(binding_txt, txt_name)
                    # 写入文件
                    with open(txt_path, "w", encoding="utf-8") as txt:
                        txt.write(text_result)
                    """
                except Exception as e:
                    InfoBar.error(
                        title='保存发生错误',
                        content=str(e),
                        orient=Qt.Horizontal,
                        # orient=Qt.Vertical,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=-1,  # -1不会自动消失
                        parent=self
                    )
            else:
                InfoBar.warning(
                    title='文本为空',
                    content='没有需要保存的内容',
                    orient=Qt.Horizontal,
                    # orient=Qt.Vertical,
                    isClosable=False,
                    position=InfoBarPosition.BOTTOM,
                    duration=3000,  # -1不会自动消失
                    parent=self
                )


# SubBookShelf 页面卡片的逻辑
class FolderCard(ElevatedCardWidget):
    # 定义信号，待写，当点击取书时候触发，将路径传给TreeWidget；当点击还书时候触发，将路径从TreeWidget剔除
    book = Signal(str, bool)

    def __init__(self, folder_name, parent=None):
        super().__init__(parent=parent)
        self._folderName = ""

        self.initUI()
        self.load()

        self.folderName = folder_name

    def load(self):
        self.tgCtl.toggled.connect(self.ctlToggled)

    @property
    def folderName(self):
        return self._folderName

    @folderName.setter
    def folderName(self, value: str):
        self.lbFolderName.setText(value)
        self._folderName = value

    def ctlToggled(self, state: bool):
        binding_folder = r"binding"
        reading_folder = r"reading"
        if state:
            self.source_folder = os.path.join(binding_folder, self.folderName)
            self.target_folder = os.path.join(reading_folder, self.folderName)
            self.moveBookToReading()
        else:
            self.source_folder = os.path.join(reading_folder, self.folderName)
            self.target_folder = os.path.join(binding_folder, self.folderName)
            self.moveBookToBinding()

    def moveBookToReading(self):
        self.copyBook()
        TeachingTip.create(
            target=self.lbFolderName,
            icon=InfoBarIcon.SUCCESS,
            title='『' + str(self.folderName) + '』 ' + '  取书成功',
            content="请前往阅读页面查看书籍",
            isClosable=False,  # 右上角关闭按钮不显示
            tailPosition=TeachingTipTailPosition.TOP,
            duration=3000,
            parent=self
        )

    def moveBookToBinding(self):
        self.moveBook()
        TeachingTip.create(
            target=self.lbFolderName,
            icon=InfoBarIcon.SUCCESS,
            title='『' + str(self.folderName) + '』 ' + '  还书成功',
            content="下次阅读前请先从书架上取书",
            isClosable=False,  # 右上角关闭按钮不显示
            tailPosition=TeachingTipTailPosition.TOP,
            duration=6000,
            parent=self
        )

    def copyBook(self):
        if os.path.exists(self.source_folder):
            try:
                if os.path.exists(self.target_folder):
                    shutil.rmtree(self.target_folder)
                    shutil.copytree(self.source_folder, self.target_folder)
                else:
                    shutil.copytree(self.source_folder, self.target_folder)
            except Exception as e:
                signalBus.showInfoBar.emit(InfoBarMsgModel(
                    title="取书失败",
                    content=f"{str(self.folderName)}:{str(e)}",
                    type="error",
                    duration=-1,
                    position=InfoBarPosition.BOTTOM
                ))
        else:
            signalBus.showInfoBar.emit(InfoBarMsgModel(
                title='路径不存在',
                type="error",
                content='请检查 ' + str(self.source_folder) + ' 是否正确',
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,  # 不会自动消失
            ))

    def moveBook(self):
        if os.path.exists(self.source_folder):
            try:
                if os.path.exists(self.target_folder):
                    shutil.rmtree(self.target_folder)
                    shutil.move(self.source_folder, self.target_folder)
                else:
                    shutil.move(self.source_folder, self.target_folder)
            except Exception as e:
                signalBus.showInfoBar.emit(InfoBarMsgModel(
                    title="还书失败",
                    content=f"{str(self.folderName)}:{str(e)}",
                    type="error",
                    duration=-1,
                    position=InfoBarPosition.BOTTOM
                ))
        else:
            signalBus.showInfoBar.emit(InfoBarMsgModel(
                title='路径不存在',
                type="error",
                content='请检查 ' + str(self.source_folder) + ' 是否正确',
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,  # 不会自动消失
            ))


    def initUI(self):
        self.setStyleSheet("padding: 10px; margin: 5px;")
        self.setFixedSize(220, 300)
        layout = QHBoxLayout(self)
        self.lbFolderName = StrongBodyLabel(self)
        self.lbFolderName.setFixedWidth(220)
        self.tgCtl = PillPushButton('取書')

        layout.addWidget(self.lbFolderName)
        layout.addWidget(self.tgCtl)
        layout.setAlignment(self.tgCtl, Qt.AlignBottom)
        layout.setAlignment(self.lbFolderName, Qt.AlignTop)


class SubBookShelf(BookShelfUi, QWidget):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        # 创建滚动区域
        self.scroll_area = QWidget()
        self.SmoothScrollArea.setWidgetResizable(True)
        self.SmoothScrollArea.setWidget(self.scroll_area)
        self.SmoothScrollArea.setStyleSheet("QScrollArea { background-color: white; }")
        # 创建主布局
        self.card_layout = FlowLayout(self.scroll_area)
        # self.CardWidget = QGridLayout(self)
        # 2024-11-05 程序优化，路径改为相对路径，便于后续文件夹的创建和移动
        self.base_path = Path('../OCR/binding')

        self.initFolderCard()
        # 将滚动区域添加到主布局
        self.scroll_area.setLayout(self.card_layout)
        self.setObjectName(text.replace(' ', '-'))

        self.SearchLineEdit.textChanged.connect(self.filter_book)

        # 创建文件系统监视器
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(str(self.base_path))  # 监视整个文件夹
        # 连接文件夹变化的信号
        self.file_watcher.directoryChanged.connect(self.directory_changed)

    def initFolderCard(self):
        """
        初始化card到grid
        :return:
        """

        for folderPath in self.base_path.iterdir():
            if not folderPath.is_dir():
                continue
            card = FolderCard(folderPath.name, parent=self)
            self.card_layout.addWidget(card)

    def directory_changed(self):
        # 目录变化时刷新 TreeWidget
        self.onFolderChangeRefresh()

    def onFolderChangeRefresh(self):
        # 更新 SubBookShelf 页面中的卡片视图，显示 `base_path` 文件夹内的子文件夹。

        # 获取当前grid里所有FolderCard元素
        existCardWidgets: List[FolderCard] = [self.card_layout.itemAt(i).widget() for i in range(self.card_layout.count()) if isinstance(self.card_layout.itemAt(i).widget(), FolderCard)]
        existFolderName = set([i.folderName for i in existCardWidgets])

        # 获取最新文件夹名
        latestFolderName = set([i.name for i in self.base_path.iterdir()])

        # 新增文件名
        newFolder = list(latestFolderName - existFolderName)
        # 移除文件名
        deletedFolder = list(existFolderName - latestFolderName)

        for folderName in deletedFolder:
            card = next(i for i in existCardWidgets if i.folderName == folderName)
            card.deleteLater()

        for folderName in newFolder:
            card = FolderCard(folderName, parent=self)
            self.card_layout.addWidget(card)

    # 遍历 CardWidget，如果文件夹名包含搜索内容则显示，否则隐藏
    def filter_book(self):
        # todo
        name = self.SearchLineEdit.text()

        for i in range(self.card_layout.count()):
            widget = self.card_layout.itemAt(i).widget()
            folder_name = widget.folderName
            if name in folder_name:
                widget.show()
            else:
                widget.hide()




# 2024-12-11重写古典阅读模式，增加竖条仿古
class VerticalColumnTextEdit(PlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.column_width = 50  # 每列宽度
        self.line_height = self.fontMetrics().height() + 5  # 行高，字与字之间隔开5px，阅读更舒适
        self.margin = 2  # 边距
        self.cursor_blink_timer = QTimer(self)
        self.cursor_blink_timer.setInterval(500)  # 光标闪烁间隔
        self.cursor_blink_timer.timeout.connect(self.toggle_cursor_visibility)
        self.cursor_visible = True
        self.document().contentsChanged.connect(self.update_cursor_position)
        self.cursor_position = None  # 当前光标的位置 (x, y)
        # 启动光标闪烁定时器
        self.cursor_blink_timer.start()

    # 重写paint事件，实现竖向排版
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setFont(self.font())
        metrics = QFontMetrics(self.font())

        # 计算可用绘制区域
        rect = self.contentsRect().adjusted(self.margin, self.margin, -self.margin, -self.margin)
        max_height = rect.height()
        max_width = rect.width()
        current_x = rect.right() - self.column_width  # 从最右边开始
        current_y = rect.top()  # 从顶部开始
        column_count = 0

        text = self.toPlainText()
        cursor = self.textCursor()
        cursor_pos = cursor.position()

        char_index = 0
        for char in text:
            if char == '\n':  # 忽略换行符
                continue
            elif current_y + self.line_height > max_height:  # 如果当前列高度超出可用高度
                current_x -= self.column_width  # 开始新列
                current_y = rect.top()  # 重置 y 坐标为顶部
                column_count += 1
                if current_x < rect.left():  # 如果超过了最大列数，停止绘制
                    break

            # 绘制单个字符
            painter.drawText(QRectF(current_x, current_y, self.column_width, self.line_height), Qt.AlignCenter | Qt.AlignVCenter, char)

            # 更新光标位置
            if char_index == cursor_pos - 1:
                self.cursor_position = (current_x, current_y)
            char_index += 1

            current_y += self.line_height  # 下移一行

        # 在每列的右边画竖线作为分隔线
        if column_count > 0:
            pen = QPen(QColor(Qt.black))
            pen.setWidth(1)
            painter.setPen(pen)
            for col in range(1, column_count + 1):
                line_x = rect.right() - (col * self.column_width)
                painter.drawLine(line_x, rect.top(), line_x, rect.bottom())

        # 绘制光标
        if self.cursor_position and self.cursor_visible:
            cursor_rect = QRectF(self.cursor_position[0], self.cursor_position[1], 2, self.line_height)
            pen = QPen(QColor(Qt.black))
            pen.setWidth(2)  # 设置光标的宽度
            painter.setPen(pen)
            painter.drawLine(cursor_rect.topLeft(), cursor_rect.bottomLeft())

    def toggle_cursor_visibility(self):
        self.cursor_visible = not self.cursor_visible
        self.viewport().update()  # 触发重绘

    def update_cursor_position(self):
        cursor = self.textCursor()
        cursor_pos = cursor.position()
        self.viewport().update()  # 触发重绘以更新光标位置

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.update_cursor_position()  # 确保每次按键后都更新光标位置

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.cursor_visible = True
        self.viewport().update()  # 确保获得焦点时光标可见

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.cursor_visible = False
        self.viewport().update()

class SubRead(ReadUi, QWidget):
    # 2024-11-05 程序优化，路径改为相对路径，便于后续文件夹的创建和移动
    my_data_dct = {"dir": "../OCR/reading", "uuid": {}, "txt": {}}
    scdj = ""

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.show_flag = 0
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))
        self.TreeWidBook.itemClicked.connect(self.clickeditems)

        self.TreeWidBook.setColumnCount(3)
        self.TreeWidBook.setHeaderLabels(["我的藏书", "描述", ""])
        header = self.TreeWidBook.header()
        header.hideSection(1)
        header.hideSection(2)
        self.TreeWidBook.setColumnWidth(1, 1)
        self.TreeWidBook.setColumnWidth(1, 2)

        # 替换成根目录路径
        self.root_dir = self.my_data_dct["dir"]
        # 如果不存在则创建目录
        self.create_dir(self.root_dir)
        # 从根节点开始填充
        self.populate_tree(self.root_dir, self.TreeWidBook.invisibleRootItem())

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(self.root_dir)  # 监视整个文件夹
        # 连接文件夹变化的信号
        self.file_watcher.directoryChanged.connect(self.refresh_tree)
        # self.frame_2.setStyleSheet("border: 1px solid red;")  # 设置边框为1px宽的红色实线
        self.show()
        self.SearchLineEdit.textChanged.connect(self.filter_book)

        # 2024-12-06 在SubApplication中实例化SettingsManager
        self.settings_manager = SettingsManager('settings')
        # 连接信号
        self.settings_manager.settingVar.connect(self.receivedReadSettings)
        # 从文件加载设置并发射信号
        self.settings_manager.loadSettings()

        # 接收设置并实例化变量
        self.PlainTextClassic = VerticalColumnTextEdit(self)
        layout = QVBoxLayout()
        layout.addWidget(self.PlainTextClassic)
        self.PlainText.setLayout(layout)
        self.PlainText.setReadOnly(True)
        self.PlainTextClassic.setReadOnly(True)
        self.PlainText.setFocusPolicy(Qt.NoFocus)
        self.PlainTextClassic.setFocusPolicy(Qt.NoFocus)


    def receivedReadSettings(self, settings):
        # 信号接收到settings并逐个实例化成变量，供SubRead调用
        for key, value in settings.items():
            setattr(self, key, value)
        self.read_font_family = self.font_family
        self.read_font_size = self.font_size
        self.read_status_C = self.status_C
        self.read_status_M = self.status_M


    def refresh_tree(self):
        self.TreeWidBook.clear()
        # 重新填充树
        self.populate_tree(self.root_dir, self.TreeWidBook.invisibleRootItem())

    # 2024-11-05 程序优化，便于后续文件夹的创建和移动，为update_TreeWidget前置条件
    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except Exception as e:
                InfoBar.error(
                    title='创建目录时出错',
                    content=str(e),
                    orient=Qt.Horizontal,
                    # orient=Qt.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,  # -1不会自动消失
                    parent=self
                )
        else:
            InfoBar.success(
                title='路径已存在',
                content=str(dir_path) + ' 系统曾创建过',
                orient=Qt.Horizontal,
                # orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=3000,  # -1不会自动消失
                parent=self
            )

    def populate_tree(self, dir_path, parent_item):
        """递归填充树控件"""
        txt_data = ""
        for item_name in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item_name)
            if ".txt" in item_path:
                with open(item_path, "r", encoding="utf-8") as f:
                    txt_data += f.read()
        short_ida = shortuuid.uuid()  # 生成 22 位的短 UUID
        self.my_data_dct["txt"][short_ida] = txt_data

        for item_name in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item_name)
            if os.path.isfile(item_path):
                hzm = str(item_path).split(".")[-1]
                if not hzm in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'tga']:
                    continue
            item = QTreeWidgetItem(parent_item)
            # 显示路径和uuid对应关系
            # print("wty:", dir_path, "a", item_path)
            item.setText(0, item_name)
            short_id = shortuuid.uuid()  # 生成 22 位的短 UUID
            self.my_data_dct["uuid"][short_id] = item_path
            item.setText(1, short_id)
            item.setText(2, short_ida)

            if os.path.isdir(item_path):
                self.populate_tree(item_path, item)  # 递归处理子目录

    def addPixmap(self, parent, filename):
        item = QTreeWidgetItem(parent)
        item.setText(0, os.path.basename(filename))
        # 如果需要在TreeWidget中显示图片，可以使用以下代码
        # item.setIcon(0, QIcon(filename))
        parent.addChild(item)

    def addPixmaps(self, parent, directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # 图片格式后续按需调整
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tga')):
                self.addPixmap(parent, filepath)

    def clickeditems(self):
        item = self.TreeWidBook.currentItem().text(0)
        item2 = self.TreeWidBook.currentItem().text(1)
        item3 = self.TreeWidBook.currentItem().text(2)

        if not self.scdj == item3:
            txt_data = self.my_data_dct["txt"][item3]
            if self.read_status_C == True:
                self.PlainTextClassic.setPlainText(txt_data)
                font = QFont(self.read_font_family, self.read_font_size)
                self.PlainTextClassic.setFont(font)

            else:
                self.PlainText.setPlainText(txt_data)
                font = QFont(self.read_font_family, self.read_font_size)
                self.PlainText.setFont(font)
                self.PlainTextClassic.hide()
            self.scdj = item3

        paths_img = self.my_data_dct["uuid"][item2]
        if not any(ext in str(paths_img).lower() for ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tga')):
            return
        self.show_reading_img(paths_img)

    def show_reading_img(self, image_file):
        if self.show_flag == 0:
            horizontalLayout_22 = QHBoxLayout(self.frame_2)
            self.graphics_layout = pg.GraphicsLayoutWidget()
            self.graphics_layout.setBackground("w")
            horizontalLayout_22.addWidget(self.graphics_layout)

            self.view_box = self.graphics_layout.addViewBox()
            self.view_box.setAspectLocked(True)  # 锁定纵横比
            self.view_box.setBackgroundColor('w')
            # 处理文件不存在的情况
            try:
                pixmap = QPixmap(image_file)
                image = pixmap.toImage()
                image_array = pg.imageToArray(image, copy=True)
                # image_array = np.flipud(image_array)  # 垂直翻转 numpy 数组
                image_array = np.fliplr(image_array)  # 水平翻转 numpy 数组
                self.image_item = pg.ImageItem(image_array)
                # self.view_box.addItem(image_array)
                self.view_box.addItem(self.image_item)
            except FileNotFoundError:
                InfoBar.error(
                    title='指定的文件不存在',
                    content=str(image_file) + ' 未找到',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,
                    parent=self
                )
            # 显示完图片后，show_flag置1，避免重复
            self.show_flag = 1
        else:
            pixmap = QPixmap(image_file)
            image = pixmap.toImage()
            image_array = pg.imageToArray(image, copy=True)
            image_array = np.fliplr(image_array)  # 水平翻转 numpy 数组
            # image_item = pg.ImageItem(image_array)
            self.image_item.setImage(image_array)  # 更新图片
            self.view_box.autoRange()  # 自动调整视图范围

    def filter_book(self):
        name = self.SearchLineEdit.text()
        # card_list = []
        count = self.TreeWidBook.topLevelItemCount()
        # 由于TreeWidget和SmoothScrollArea控件本质不同，所以filter_book()隐藏和显示的逻辑不同
        for i in range(count):
            widget = self.TreeWidBook.topLevelItem(i)
            folder_name = widget.text(0).lower()
            if name in folder_name:
                widget.setHidden(False)  # 显示匹配项
            else:
                widget.setHidden(True)  # 隐藏不匹配项





class SubSetting(SetUi, QWidget):
    settingVar = Signal(dict)  # 定义信号，将设置参数以字典形式传递

    settings = {
    "font_family": ["Microsoft YaHei UI"],
    "font_size": 9,
    "color": "#009faa",
    "confidence": 1.0,
    "ocrs": "\u767e\u5ea6OCR",
    "status_C": True,
    "status_M": False,
    "path": ""
    }

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.pBtn_Font.clicked.connect(self.chooseFont)
        self.pBtn_Color.clicked.connect(self.chooseColor)
        self.DSpinBox_acc.valueChanged.connect(self.confidence)
        self.ComboBox_OCRS.addItems(['百度OCR', '腾讯OCR', '阿里OCR', '常中医OCR'])
        self.ComboBox_OCRS.currentTextChanged.connect(self.ocrSouce)
        self.LineEdit_Path.textChanged.connect(self.savePath)
        self.RadioButton_C.toggled.connect(self.readClassic)
        self.RadioButton_M.toggled.connect(self.readModern)
        self.setObjectName(text.replace(' ', '-'))

        self.loadSettings('settings')

    def chooseFont(self):
        ok, font = QFontDialog.getFont()
        # 检查用户是否选择了字体
        if ok:
            font_family = font.family()
            font_size = font.pointSize()
            self.pBtn_Font.setText(f"{font_family}      {font_size}px")
            self.updateSettings('font_family', font_family)
            self.updateSettings('font_size', font_size)
            # return font_family, font_size
        else:
            InfoBar.warning(
                title='字体未选择',
                content='将以当前字体显示',
                orient=Qt.Vertical,
                isClosable=False,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            return
    def chooseColor(self):
        color = QColorDialog.getColor()
        ok = color.isValid()
        if ok:
            self.pBtn_Color.setStyleSheet(f"border-radius: 5px; background: {color.name()};")
            self.settings['color'] = color.name()
            self.updateSettings('color', color.name())
            # return color

    def confidence(self):
        confidence = self.DSpinBox_acc.value()
        self.updateSettings('confidence', confidence)
        # return confidence

    def ocrSouce(self):
        ocrs = self.ComboBox_OCRS.currentText()
        self.updateSettings('ocrs', ocrs)
        # return ocrs

    def savePath(self):
        # 保存路径
        path = self.LineEdit_Path.text()
        self.updateSettings('path', path)
        # return path

    def readClassic(self):
        # 阅读模式切换
        status_C = self.RadioButton_C.isChecked()
        self.updateSettings('status_C', status_C)
        # text_C = self.RadioButton_C.text()
        # return status_C
    def readModern(self):
        # 阅读模式切换
        status_M = self.RadioButton_M.isChecked()
        self.updateSettings('status_M', status_M)
        # text_M = self.RadioButton_M.text()
        # return status_M

    # 更新 settings 字典对应键值对
    def updateSettings(self, key, value):
        self.settings[key] = value
        self.saveSettings(self.settings, 'settings')

    # 保存设置到 JSON 文件
    def saveSettings(self, settings, file_path):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(settings, json_file, indent=4)
        except Exception as e:
            InfoBar.error(
                title='保存设置文件异常',
                content=str(e),
                orient=Qt.Horizontal,
                # orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,  # -1不会自动消失
                parent=self
            )

    # 从 JSON 文件读取设置
    def loadSettings(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as json_file:
                    settings = json.load(json_file)
                    # 如果不符合就else为默认格式
                    if "font_family" in settings and "font_size" in settings:
                        self.pBtn_Font.setText(f"{settings['font_family']}      {settings['font_size']}px")
                    else:
                        self.pBtn_Font.setText("选择字体")

                    if "color" in settings:
                        self.pBtn_Color.setStyleSheet(f"border-radius: 5px; background: {settings['color']};")
                    else:
                        self.pBtn_Color.setStyleSheet(f"border-radius: 5px; background: '#009faa';")

                    if "confidence" in settings:
                        self.DSpinBox_acc.setValue(settings['confidence'])
                    else:
                        self.DSpinBox_acc.setValue(1.00)

                    if "ocrs" in settings:
                        self.ComboBox_OCRS.setCurrentText(settings['ocrs'])
                    else:
                        self.ComboBox_OCRS.setCurrentIndex(0)

                    if "path" in settings:
                        self.LineEdit_Path.setText(settings['path'])
                    else:
                        self.LineEdit_Path.setText("")

                    if "status_C" in settings:
                        self.RadioButton_C.setChecked(settings['status_C'])
                    else:
                        self.RadioButton_C.setChecked(True)

                    if "status_M" in settings:
                        self.RadioButton_M.setChecked(settings['status_M'])
                    else:
                        self.RadioButton_M.setChecked(False)
                    # 更新字典
                    #self.settings.update(settings)
            else:
                InfoBar.error(
                    title='设置文件缺失',
                    content='文件' + str(file_path) + '不存在',
                    orient=Qt.Horizontal,
                    # orient=Qt.Vertical,
                    isClosable=False,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=3000,  # -1不会自动消失
                    parent=self
                )
        except Exception as e:
            InfoBar.error(
                title='设置文件加载异常',
                content=str(e),
                orient=Qt.Horizontal,
                # orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,  # -1不会自动消失
                parent=self
            )



if __name__ == '__main__':
    # setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()