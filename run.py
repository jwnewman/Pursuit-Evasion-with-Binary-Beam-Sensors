import sys, math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from showsimulation import Ui_MainWindow
 
class MyForm(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.canvas = polygonWindow(self.ui.horizontalLayoutWidget)
		self.ui.horizontalLayout.addWidget(self.ui.canvas)
		QtCore.QObject.connect(self.ui.clearButton, QtCore.SIGNAL("clicked()"), self.ui.canvas.clear )
		#QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("returnPressed()"), self.add_entry)

class polygonWindow(QtGui.QGraphicsView):
	clickPos = QPointF()
	movePos = QPointF()
	initiated = 0
	clickEvent = 0
	moveEvent = 0
	vertices=[]
	numVertices = 0
	polygonFinished = 0
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setMouseTracking(1);
		
	def clear(self):
		self.clickPos = QPointF()
		self.movePos = QPointF()
		self.clickEvent = 0
		self.moveEvent = 0
		self.initiated = 0
		self.vertices=[]
		self.numVertices = 0
		self.polygonFinished = 0
		self.viewport().update()
		
	def intersect(self, center1, center2, radius):
		line = QLineF(center1, center2)
		if line.length() <= radius*2:
			return 1
		else:
			return 0
			
	def illegal(self, point):
		if self.numVertices == 0:
			return 0
		intersectionPoint = QPointF()
		newLine = QLineF(point, self.vertices[self.numVertices-1])
		for i in range(self.numVertices-1):
			existingLine = QLineF(self.vertices[i], self.vertices[i+1])
			if newLine.intersect(existingLine, intersectionPoint) == 1:
				if not intersectionPoint == newLine.p1() and not intersectionPoint == newLine.p2():
					return 1
		return 0
			
		
	def mousePressEvent(self, event):
		self.clickPos = event.posF()
		self.initiated = 1
		self.clickEvent = 1
		self.moveEvent = 0
		self.viewport().update()
		
	def mouseMoveEvent(self, event):
		self.movePos = event.posF()
		self.moveEvent = 1
		self.clickEvent = 0
		if self.initiated:
			self.viewport().update()
		
	def paintEvent(self, event):
		radius = 3
		p = QPainter(self.viewport())
		p.setPen(Qt.black)
		for i in range(self.numVertices-1):
			p.drawLine(self.vertices[i],self.vertices[i+1])
		if not self.polygonFinished:
			if self.clickEvent:
				if self.numVertices > 1:
					if self.intersect(self.vertices[0], self.clickPos, radius):
						if not self.illegal(self.clickPos):
							self.vertices.append(self.vertices[0])
							self.numVertices+=1
							p.drawLine(self.vertices[self.numVertices-2],self.vertices[0])
							self.polygonFinished = 1
							return
				if not self.illegal(self.clickPos):
					self.vertices.append(self.clickPos)
					self.numVertices+=1
					p.drawLine(self.vertices[self.numVertices-2],self.clickPos)
				else:
					self.clickPos = self.vertices[self.numVertices-1]
			if self.initiated:
				p.setBrush(QBrush(Qt.blue))
				p.drawEllipse(self.vertices[0], radius, radius)
				p.setBrush(QBrush(Qt.red))
				p.drawEllipse(self.clickPos, radius, radius)
				if self.illegal(self.movePos):
					p.setPen(Qt.red)
				p.drawLine(self.vertices[self.numVertices-1],self.movePos)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())