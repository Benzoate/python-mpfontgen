import sys
import math
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QFontDialog, QColorDialog
import mainwindow


class StartQT5(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Bitmap Font Creator')

        #Initial Values
        self.font = QFont()
        self.character_set = ('abcdefghijklmnopqrstuvwxyz'
                              'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                              '1234567890[]\'#;,./\\`¬!"£$'
                              '%^&*()_+{}:@~?><|')
        self.fill_color = QColor(0, 0, 0, 255)
        self.fill_angle = 0.0

        self.drop_shadow = True
        self.shadow_color = QColor(0, 0, 0, 127)
        self.shadow_angle = 45.0
        self.shadow_size = 3.0
        self.shadow_distance = 5.0

        self.stroke_color = QColor(255, 255, 255, 255)
        self.stroke_width = 0.0

        #Connect sockets
        self.ui.fontbutton.clicked.connect(self.font_dialog)
        self.ui.fillColorButton.clicked.connect(self.fill_color_dialog)
        self.ui.shadowColorButton.clicked.connect(self.shadow_color_dialog)
        self.ui.strokeColorButton.clicked.connect(self.stroke_color_dialog)
        self.ui.shadowAngleBox.valueChanged.connect(self.shadow_angle_changed)
        self.ui.shadowDistanceBox.valueChanged.connect(self.shadow_dist_changed)
        self.ui.shadowSizeBox.valueChanged.connect(self.shadow_size_changed)

        #Update UI
        self.update_values()

    def update_values(self):
        self.ui.characterSetBox.setPlainText(self.character_set)

        self.ui.fillColor.setStyleSheet("""
            QFrame
            {
                background-color: %s;
            }
        """ % (self.fill_color.name()))
        self.ui.fillAngleBox.setValue(self.fill_angle)

        self.ui.shadowColor.setStyleSheet("""
            QFrame{
                background-color: %s;
            }
            """ % (self.shadow_color.name()))
        self.ui.shadowAngleBox.setValue(self.shadow_angle)
        self.ui.shadowSizeBox.setValue(self.shadow_size)
        self.ui.shadowDistanceBox.setValue(self.shadow_distance)

        self.ui.strokeColor.setStyleSheet("""
            QFrame{
                background-color: %s;
            }
            """ % (self.stroke_color.name()))
        self.ui.strokeWidthBox.setValue(self.stroke_width)
        self.refresh_preview()

    def shadow_size_changed(self, value):
        self.shadow_size = float(value)
        self.refresh_preview()

    def shadow_dist_changed(self, value):
        self.shadow_distance = float(value)
        self.refresh_preview()

    def shadow_angle_changed(self, value):
        self.shadow_angle = float(value)
        self.refresh_preview()

    def shadow_color_dialog(self):
        options = QColorDialog.ShowAlphaChannel
        color = QColorDialog.getColor(initial=self.shadow_color,
                                      parent=self,
                                      options=options)
        if not color.isValid():
            return
        self.shadow_color = color
        self.update_values()

    def stroke_color_dialog(self):
        options = QColorDialog.ShowAlphaChannel
        color = QColorDialog.getColor(initial=self.stroke_color,
                                      parent=self,
                                      options=options)
        if not color.isValid():
            return
        self.stroke_color = color
        self.update_values()

    def fill_color_dialog(self):
        options = QColorDialog.ShowAlphaChannel
        color = QColorDialog.getColor(initial=self.fill_color,
                                      parent=self,
                                      options=options)

        if not color.isValid():
            return

        self.fill_color = color
        self.update_values()

    def font_dialog(self):
        font, ok = QFontDialog.getFont(QFont(), self)
        if ok:
            self.font = font

    def get_path_for_char(self, char, baseline):
        ret = []
        font_info = QFontMetrics(self.font)
        if self.ui.dropShadowGroupBox.isChecked():
            shadow_baseline = QtCore.QPointF(baseline)
            shadow_font_path = QPainterPath()
            shadow_font_brush = QBrush(self.shadow_color, QtCore.Qt.SolidPattern)
            shadow_offsetx = (math.sin(self.shadow_angle *
                                       ((2.0 * math.pi)/360.0)) *
                              self.shadow_distance)
            shadow_offsety = (math.cos(self.shadow_angle *
                                       ((2.0 * math.pi)/360.0)) *
                              self.shadow_distance)
            shadow_baseline.setX(shadow_baseline.x() + shadow_offsetx)
            shadow_baseline.setY(shadow_baseline.y() + shadow_offsety)
            shadow_font_path.addText(shadow_baseline, self.font, char)
            stroker = QPainterPathStroker()
            stroker.setWidth(self.shadow_size)
            stroker.setJoinStyle(QtCore.Qt.MiterJoin)
            shadow_font_path += stroker.createStroke(shadow_font_path)
            ret.append((shadow_font_path, shadow_font_brush))


        main_font_path = QPainterPath()
        main_font_brush = QBrush(self.fill_color, QtCore.Qt.SolidPattern)
        main_font_path.addText(baseline, self.font, char)
        ret.append((main_font_path, main_font_brush))
        if self.ui.strokeGroupBox.isChecked():
            pass
        return ret

    def refresh_preview(self):
        font_info = QFontMetrics(self.font)
        characters = ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']

        paths_brushes = []
        last_base_x = 0.0

        for idx, char in enumerate(characters):
            if idx != 0 and idx % 4 == 0:
                last_base_x = 0
            baseline = QtCore.QPointF(last_base_x,
                                     (1+int(idx/4)) * (font_info.height()
                                                  + font_info.leading()))
            for path, brush in self.get_path_for_char(char, baseline):
                paths_brushes.append((path, brush))
            last_base_x += font_info.width(char)
        self.ui.widget.setPathBrush(paths_brushes)


a = QApplication(sys.argv)

w = StartQT5()
w.show()


sys.exit(a.exec_())
