from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *

from PyQt5 import QtCore

class QPaintArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.path_brush = []

    def setPathBrush(self, path_brush):
        self.path_brush = path_brush
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setPen(QColor(0,0,0,0))
        for path, brush in self.path_brush:
            painter.setBrush(brush)
            painter.drawPath(path)
