import polygon
import pursuitStrategy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class controller():
	PIXELS_PER_UNIT_DISTANCE = 5.0
	strategy = pursuitStrategy.pursuitStrategy()
	
	def __init__(self):
		return
		
	def startPursuitStrategy(self, pursuerCoord, evaderCoord, p, beams, h):
		vertices = []
		poly = polygon.polygon(vertices)
		pCoord = QPointF()
		eCoord = QPointF()
		pCoord = pursuerCoord/self.PIXELS_PER_UNIT_DISTANCE
		eCoord = evaderCoord/self.PIXELS_PER_UNIT_DISTANCE
		bLines = []
		hLines = []
		for vertex in p:
			vertices.append(QPointF(vertex.x()/self.PIXELS_PER_UNIT_DISTANCE, vertex.y()/self.PIXELS_PER_UNIT_DISTANCE))
			poly.append(QPointF(vertex.x()/self.PIXELS_PER_UNIT_DISTANCE, vertex.y()/self.PIXELS_PER_UNIT_DISTANCE))
		for beam in beams:
			bLines.append(QLineF(beam.p1().x()/self.PIXELS_PER_UNIT_DISTANCE, beam.p1().y()/self.PIXELS_PER_UNIT_DISTANCE, beam.p2().x()/self.PIXELS_PER_UNIT_DISTANCE, beam.p2().y()/self.PIXELS_PER_UNIT_DISTANCE))
		for cut in h:
			hLines.append(QLineF(cut.p1().x()/self.PIXELS_PER_UNIT_DISTANCE, cut.p1().y()/self.PIXELS_PER_UNIT_DISTANCE, cut.p2().x()/self.PIXELS_PER_UNIT_DISTANCE, cut.p2().y()/self.PIXELS_PER_UNIT_DISTANCE))
		
		self.strategy = pursuitStrategy.pursuitStrategy(pCoord, eCoord, poly, bLines, hLines)
		
	def getCriticalBeam(self):
		beam = self.strategy.getCriticalBeam()
		beam = QLineF(beam.p1().x()*self.PIXELS_PER_UNIT_DISTANCE, beam.p1().y()*self.PIXELS_PER_UNIT_DISTANCE, beam.p2().x()*self.PIXELS_PER_UNIT_DISTANCE, beam.p2().y()*self.PIXELS_PER_UNIT_DISTANCE)
		return beam
			