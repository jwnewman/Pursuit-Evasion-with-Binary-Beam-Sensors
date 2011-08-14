import math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class polygon(QPolygonF):
	def __init__(self, vertices=[]):
		self.vertices=vertices
		QPolygonF.__init__(self, vertices)
		
	def getVertices(self):
		return self.vertices
		
	def isClockwise(self):
		br = 0
		for i in range(1,len(self.vertices)-1):
			if self.vertices[i].y() < self.vertices[br].y() or (self.vertices[i].y() == self.vertices[br].y() and self.vertices[i].x() > self.vertices[br].x()):
				br = i
		return self.right(br)
		
	def area(self, a, b, c):
		return ((b.x() - a.x())*(c.y() - a.y())) - ((c.x() - a.x())*(b.y() - a.y()))
		
	def right(self, i):
		a = self.vertices[i-1]
		b = self.vertices[i]
		c = self.vertices[i+1]
		if i == 0:
			a = self.vertices[len(self.vertices)-2]
		return self.area(a, b, c) < 0
		
	def left(self, i):
		a = self.vertices[i-1]
		b = self.vertices[i]
		c = self.vertices[i+1]
		if i == 0:
			a = self.vertices[len(self.vertices)-2]
		return self.area(a, b, c) > 0
		
	def reflex(self, i):
		if not self.isClockwise():
			return self.right(i)
		else:
			return self.left(i)
			
	def pointsRight(self, beam, extBeam):
		if beam == extBeam:
			return 0
		if beam.p1() == extBeam.p1():
			vertexIndex = self.vertices.index(beam.p2())
		else:
			vertexIndex = self.vertices.index(beam.p1())
		a = self.vertices[vertexIndex-1]
		b = self.vertices[vertexIndex]
		c = self.vertices[vertexIndex+1]
		if vertexIndex == 0:
			a = self.vertices[len(self.vertices)-2]
		if a.x() < b.x() and c.x() < b.x():
			return 1
		else:
			return 0
			
	def pointsUp(self, hCut, extCut):
		if hCut == extCut:
			return 0
		if hCut.p1() == extCut.p1():
			vertexIndex = self.vertices.index(hCut.p2())
		else:
			vertexIndex = self.vertices.index(hCut.p1())
		a = self.vertices[vertexIndex-1]
		b = self.vertices[vertexIndex]
		c = self.vertices[vertexIndex+1]
		if vertexIndex == 0:
			a = self.vertices[len(self.vertices)-2]
		if a.y() < b.y() and c.y() < b.y():
			return 1
		else:
			return 0
			
	def beamIntersectsWithEdge(self, beam, edge, intersectionPoint):
		if beam.intersect(edge, intersectionPoint) == QLineF.BoundedIntersection:
			return 1
		if beam.intersect(edge, intersectionPoint) == QLineF.UnboundedIntersection:
			if edge.p1().x() <= beam.p1().x() and edge.p2().x() >= beam.p1().x() or edge.p1().x() >= beam.p1().x() and edge.p2().x() <= beam.p1().x():
				if round(beam.p1().y(), 3) == round(intersectionPoint.y(),3) or round(beam.p2().y(), 3) == round(intersectionPoint.y(), 3):
					return 1
		return 0
		
	def hCutIntersectsWithEdge(self, hCut, edge, intersectionPoint):
		if hCut.intersect(edge, intersectionPoint) == QLineF.BoundedIntersection:
			return 1
		if hCut.intersect(edge, intersectionPoint) == QLineF.UnboundedIntersection:
			if edge.p1().y() <= hCut.p1().y() and edge.p2().y() >= hCut.p1().y() or edge.p1().y() >= hCut.p1().y() and edge.p2().y() <= hCut.p1().y():
				if round(hCut.p1().x(), 3) == round(intersectionPoint.x(),3) or round(hCut.p2().x(), 3) == round(intersectionPoint.x(), 3):
					return 1
		return 0
		
	def edgeFromBeamIntersectionPoint(self, line, point, direction, counterclockwise):
		intersectionPoint = QPointF()
		intersectionLine = QLineF()
		if counterclockwise:
			for i in range(len(self.vertices)-1):
				currentEdge = QLineF(self.vertices[i], self.vertices[i+1])
				if self.beamIntersectsWithEdge(line, currentEdge, intersectionPoint):
					if round(intersectionPoint.x(), 3) == round(point.x(), 3) and round(intersectionPoint.y(), 3) == round(point.y(), 3):
						intersectionLine = QLineF(intersectionPoint, currentEdge.p2())
		else:
			for i in range(len(self.vertices)-1,0,-1):
				currentEdge = QLineF(self.vertices[i], self.vertices[i-1])
				if self.beamIntersectsWithEdge(line, currentEdge, intersectionPoint):
					if round(intersectionPoint.x(), 3) == round(point.x(), 3) and round(intersectionPoint.y(), 3) == round(point.y(), 3):
						intersectionLine = QLineF(intersectionPoint, currentEdge.p2())
		return intersectionLine
				
	def edgeFromHCutIntersectionPoint(self, line, point, direction, counterclockwise):
		intersectionPoint = QPointF()
		intersectionLine = QLineF()
		if counterclockwise:
			for i in range(len(self.vertices)-1):
				currentEdge = QLineF(self.vertices[i], self.vertices[i+1])
				if self.hCutIntersectsWithEdge(line, currentEdge, intersectionPoint):
					if round(intersectionPoint.x(), 3) == round(point.x(), 3) and round(intersectionPoint.y(), 3) == round(point.y(), 3):
						intersectionLine = QLineF(intersectionPoint, currentEdge.p2())
		else:
			for i in range(len(self.vertices)-1,0,-1):
				currentEdge = QLineF(self.vertices[i], self.vertices[i-1])
				if self.hCutIntersectsWithEdge(line, currentEdge, intersectionPoint):
					if round(intersectionPoint.x(), 3) == round(point.x(), 3) and round(intersectionPoint.y(), 3) == round(point.y(), 3):
						intersectionLine = QLineF(intersectionPoint, currentEdge.p2())
		return intersectionLine
		
	def getLargestYVertex(self):
		largestVertex = self.vertices[0]
		for vertex in self.vertices:
			if vertex.y() > largestVertex.y():
				largestVertex = vertex
		return largestVertex
	
	def getSmallestYVertex(self):
		smallestVertex = self.vertices[0]
		for vertex in self.vertices:
			if vertex.y() < smallestVertex.y():
				smallestVertex = vertex
		return smallestVertex
	
	def getLargestXVertex(self):
		largestVertex = self.vertices[0]
		for vertex in self.vertices:
			if vertex.x() > largestVertex.x():
				largestVertex = vertex
		return largestVertex
	
	def getSmallestXVertex(self):
		smallestVertex = self.vertices[0]
		for vertex in self.vertices:
			if vertex.x() < smallestVertex.x():
				smallestVertex = vertex
		return smallestVertex
		
	def getMidpoint(self, line):
		return QPointF((line.x1()+line.x2())/2.0,(line.y1()+line.y2())/2.0)
		
	def getBeams(self, beams):
		for i in range(len(self.vertices)-1):
			if self.reflex(i):
				intersectionPoint = QPointF()
				tempBeam = QLineF(self.vertices[i].x(), self.getLargestYVertex().y(), self.vertices[i].x(), self.getSmallestYVertex().y())
				closestLargeIntersection = QPointF(tempBeam.p1().x(),tempBeam.p1().y()+1)
				closestSmallIntersection = QPointF(tempBeam.p2().x(),tempBeam.p2().y()-1)
				for j in range(len(self.vertices)-1):
					edge = QLineF(self.vertices[j], self.vertices[j+1])
					if tempBeam.intersect(edge, intersectionPoint) == QLineF.BoundedIntersection:
						if round(intersectionPoint.y(),3) > self.vertices[i].y() and round(intersectionPoint.y(),3) <= closestLargeIntersection.y():
							closestLargeIntersection = QPointF(intersectionPoint.x(), intersectionPoint.y())
						elif round(intersectionPoint.y(),3) < self.vertices[i].y() and round(intersectionPoint.y(),3) >= closestSmallIntersection.y():
							closestSmallIntersection = QPointF(intersectionPoint.x(), intersectionPoint.y())
				if not self.containsPoint(self.getMidpoint(QLineF(closestLargeIntersection,self.vertices[i])), Qt.OddEvenFill):
					closestLargeIntersection = self.vertices[i]
				if not self.containsPoint(self.getMidpoint(QLineF(closestSmallIntersection,self.vertices[i])), Qt.OddEvenFill):
					closestSmallIntersection = self.vertices[i]
				beam1 = QLineF(closestSmallIntersection, self.vertices[i])
				beam2 = QLineF(self.vertices[i], closestLargeIntersection)
				if beam1 and not beam1 in beams:
					beams.append(beam1)
				if beam2 and not beam2 in beams:
					beams.append(beam2)
		
	def getH(self, h):
		for i in range(len(self.vertices)-1):
			if self.reflex(i):
				intersectionPoint = QPointF()
				tempH = QLineF(self.getLargestXVertex().x(), self.vertices[i].y(), self.getSmallestXVertex().x(), self.vertices[i].y())
				closestLargeIntersection = QPointF(tempH.p1().x()+1,tempH.p1().y())
				closestSmallIntersection = QPointF(tempH.p2().x()-1,tempH.p2().y())
				for j in range(len(self.vertices)-1):
					edge = QLineF(self.vertices[j], self.vertices[j+1])
					if tempH.intersect(edge, intersectionPoint) == QLineF.BoundedIntersection:
						if round(intersectionPoint.x(),3) > self.vertices[i].x() and round(intersectionPoint.x(),3) <= closestLargeIntersection.x():
							closestLargeIntersection = QPointF(intersectionPoint.x(), intersectionPoint.y())
						elif round(intersectionPoint.x(),3) < self.vertices[i].x() and round(intersectionPoint.x(),3) >= closestSmallIntersection.x():
							closestSmallIntersection = QPointF(intersectionPoint.x(), intersectionPoint.y())
				if not self.containsPoint(self.getMidpoint(QLineF(closestLargeIntersection,self.vertices[i])), Qt.OddEvenFill):
					closestLargeIntersection = self.vertices[i]
				if not self.containsPoint(self.getMidpoint(QLineF(closestSmallIntersection,self.vertices[i])), Qt.OddEvenFill):
					closestSmallIntersection = self.vertices[i]
				h1 = QLineF(closestSmallIntersection, self.vertices[i])
				h2 = QLineF(self.vertices[i], closestLargeIntersection)
				if h1 and not h1 in h:
					h.append(h1)
				if h2 and not h2 in h:
					h.append(h2)