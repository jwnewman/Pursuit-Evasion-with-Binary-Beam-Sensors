import polygon
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class polygonNode():
	p = polygon.polygon([])
	visited = 0
	safe = 0
	
	def __init__(self):
		return
		
	def getPolygon(self):
		return self.p
		
	def setPolygon(self, vert):
		self.p = polygon.polygon(vert)
		
	def hasPursuer(self, pursuerCoord):
		return self.p.containsPoint(pursuerCoord, Qt.OddEvenFill)