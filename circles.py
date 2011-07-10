# display a bunch of random circles using PyQT4
 
import random
import sys
# pray for minimal namespace conflicts
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
class DrawPoints(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('Draw random Circles')
 
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        # pen sets the edge color of the circles
        painter.setPen(Qt.black)
        w = self.size().width()
        h = self.size().height()
        # draw 150 circles of random sizes, locations and colors
        for i in range(150):
            # color uses red, green, blue values (0 to 255)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            # brush sets the fill color of the circles
            painter.setBrush(QBrush(QColor(r, g, b)))
            # get center coordinates x,y of the circle
            x = random.randint(1, w-1)
            y = random.randint(1, h-1)
            # get the radius of the circle
            radius = random.randint(5, 80)
            # to draw circles match the radius
            painter.drawEllipse(QPoint(x, y), radius, radius)
 
        painter.end()
 
 
app = QApplication(sys.argv)
dp = DrawPoints()
dp.show()
app.exec_()