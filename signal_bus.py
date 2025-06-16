from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    # 全局InforBar信息
    showInfoBar = Signal(object)


signalBus = SignalBus()