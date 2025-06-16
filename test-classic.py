from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PySide6.QtGui import QPainter, QFont, QFontMetrics, QColor, QPen
from PySide6.QtCore import Qt, QRectF, QTimer

class VerticalColumnTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("SimSun", 14))  # 使用宋体，字号 14
        self.column_width = 50  # 每列宽度
        self.line_height = self.fontMetrics().height() + 2  # 行高，加上一点额外的空间
        self.margin = 20  # 边距
        self.cursor_blink_timer = QTimer(self)
        self.cursor_blink_timer.setInterval(500)  # 光标闪烁间隔
        self.cursor_blink_timer.timeout.connect(self.toggle_cursor_visibility)
        self.cursor_visible = True
        self.document().contentsChanged.connect(self.update_cursor_position)
        self.cursor_position = None  # 当前光标的位置 (x, y)

        # 启动光标闪烁定时器
        self.cursor_blink_timer.start()

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
        self.viewport().update()  # 确保失去焦点时光标不可见

# 创建主窗口
app = QApplication([])

window = QWidget()
layout = QVBoxLayout(window)

# 创建垂直列排版的输入框
vertical_column_text_edit = VerticalColumnTextEdit()

vertical_column_text_edit.setPlainText("天之道，损有余辜。人之道，不足以为乐。天地不仁，以万物为刍狗。圣人之治，生而不有，为有而死。天之道，其犹张弓乎？高者抑之，下者举之；有余者损之，不足者益之。天之道，损有余而补不足。人之道则不然，损不足以奉有余。孰能有余以奉天下？唯有道者。是以圣人为而不恃，故能无为而成。")
layout.addWidget(vertical_column_text_edit)

# 设置窗口大小
window.resize(800, 400)
window.setWindowTitle('竖排文字编辑')
window.show()

app.exec()
