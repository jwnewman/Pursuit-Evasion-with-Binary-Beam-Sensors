import sys, math
import polygon
import controller
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
		QtCore.QObject.connect(self.ui.clearButton, QtCore.SIGNAL("clicked()"), self.ui.canvas.clear)
		QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"), self.saveVertices)
		QtCore.QObject.connect(self.ui.loadButton, QtCore.SIGNAL("clicked()"), self.loadVertices)
		QtCore.QObject.connect(self.ui.beamBox, QtCore.SIGNAL("stateChanged(int)"), self.ui.canvas.showBeams)
		QtCore.QObject.connect(self.ui.hBox, QtCore.SIGNAL("stateChanged(int)"), self.ui.canvas.showH)
		
	def saveVertices(self):
		vertices = self.ui.canvas.getVertices()
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.')
		fname = open(filename, 'w')
		for i in range(len(vertices)):
			fname.write(str(vertices[i].x()))
			fname.write(" ")
			fname.write(str(vertices[i].y()))
			fname.write("\n")
		fname.close()
		
	def loadVertices(self):
		vertPoint=[]
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
		fname = open(filename)
		data = fname.read()
		vertStr = data.split()
		for i in range(0,len(vertStr)-1,2):
			vertex = QPointF(float(vertStr[i]),float(vertStr[i+1]))
			vertPoint.append(vertex)
		self.ui.canvas.setVertices(vertPoint)

class polygonWindow(QtGui.QGraphicsView):
	clickPos = QPointF()
	movePos = QPointF()
	clickEvent = 0
	moveEvent = 0
	initiated = 0
	polygonFinished = 0
	evaderSet = 0
	pursuerSet = 0
	beams = 0
	h = 0
	criticalBeam = QLineF()
	beamLines = []
	hLines = []
	evaderPos = QPointF()
	pursuerPos = QPointF()
	vertices=[]
	poly = polygon.polygon(vertices)
	control = controller.controller()
	
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setMouseTracking(1);
		
	def getVertices(self):
		return self.vertices
		
	def setVertices(self, verts):
		self.clear()
		self.vertices = verts
		if self.vertices[0] == self.vertices[len(self.vertices)-1]:
			self.polygonFinished = 1
			self.poly = polygon.polygon(self.vertices)
			self.poly.getBeams(self.beamLines)
			self.poly.getH(self.hLines)
		self.viewport().update()
		
	def showBeams(self, value):
		if value == 0:
			self.beams = 0
		else:
			self.beams = 1
		self.viewport().update()
						
	def showH(self, value):
		if value == 0:
			self.h = 0
		else:
			self.h = 1
		self.viewport().update()
		
	def initiatePursuitStrategy(self):
		self.control.startPursuitStrategy(self.pursuerPos, self.evaderPos, self.poly, self.beamLines, self.hLines)
		self.criticalBeam = self.control.getCriticalBeam()
		
	def clear(self):
		self.clickPos = QPointF()
		self.movePos = QPointF()
		self.clickEvent = 0
		self.moveEvent = 0
		self.initiated = 0
		self.polygonFinished = 0
		self.evaderSet = 0
		self.pursuerSet = 0
		self.evaderPos = QPointF()
		self.pursuerPos = QPointF()
		self.vertices=[]
		self.beamLines=[]
		self.hLines=[]
		self.poly = polygon.polygon(self.vertices)
		self.criticalBeam = QLineF()
		self.viewport().update()
		
	def intersect(self, center1, center2, radius):
		line = QLineF(center1, center2)
		if line.length() <= radius*2:
			return 1
		else:
			return 0
			
	def illegal(self, point):
		if len(self.vertices) == 0:
			return 0
		intersectionPoint = QPointF()
		newLine = QLineF(point, self.vertices[len(self.vertices)-1])
		for i in range(len(self.vertices)-1):
			existingLine = QLineF(self.vertices[i], self.vertices[i+1])
			if newLine.intersect(existingLine, intersectionPoint) == QLineF.BoundedIntersection:
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
		for i in range(len(self.vertices)-1):
			p.drawLine(self.vertices[i],self.vertices[i+1])
		if self.evaderSet:
			p.setBrush(Qt.gray)
			p.drawEllipse(self.evaderPos, radius, radius)
		if self.pursuerSet:
			p.setBrush(Qt.yellow)
			p.drawEllipse(self.pursuerPos, radius, radius)
		if not self.polygonFinished:
			if self.clickEvent:
				if len(self.vertices) > 1:
					if self.intersect(self.vertices[0], self.clickPos, radius):
						if not self.illegal(self.clickPos):
							self.vertices.append(self.vertices[0])
							self.poly.append(self.vertices[0])
							p.drawLine(self.vertices[len(self.vertices)-2],self.vertices[0])
							self.polygonFinished = 1
							self.poly = polygon.polygon(self.vertices)
							self.poly.getBeams(self.beamLines)
							self.poly.getH(self.hLines)
							return
				if not self.illegal(self.clickPos):
					self.vertices.append(self.clickPos)
					p.drawLine(self.vertices[len(self.vertices)-2],self.clickPos)
				else:
					self.clickPos = self.vertices[len(self.vertices)-1]
			if self.initiated:
				p.setBrush(QBrush(Qt.blue))
				p.drawEllipse(self.vertices[0], radius, radius)
				p.setBrush(QBrush(Qt.red))
				p.drawEllipse(self.clickPos, radius, radius)
				if self.illegal(self.movePos):
					p.setPen(Qt.red)
				p.drawLine(self.vertices[len(self.vertices)-1],self.movePos)
		else:
			if not self.evaderSet:
				p.setBrush(QBrush(Qt.gray))
				p.drawEllipse(self.movePos, radius, radius)
				if self.clickEvent:
					if self.poly.containsPoint(self.clickPos, Qt.OddEvenFill):
						p.drawEllipse(self.clickPos, radius, radius)
						self.evaderPos = self.clickPos
						self.evaderSet = 1
						return
			else:
				if not self.pursuerSet:
					p.setBrush(QBrush(Qt.yellow))
					p.drawEllipse(self.movePos,radius,radius)
					if self.clickEvent:
						if self.poly.containsPoint(self.clickPos, Qt.OddEvenFill):
							p.drawEllipse(self.clickPos, radius, radius)
							self.pursuerPos = self.clickPos
							self.pursuerSet = 1
							self.initiatePursuitStrategy()
							return
			if self.beams:
				for line in self.beamLines:
					p.setPen(Qt.DashLine)
					p.drawLine(line)
			if self.h:
				for line in self.hLines:
					p.setPen(Qt.DashLine)
					p.drawLine(line)
			if self.criticalBeam:
				p.setPen(Qt.red)
				p.drawLine(self.criticalBeam)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())