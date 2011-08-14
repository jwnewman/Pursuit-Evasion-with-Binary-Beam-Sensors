import controller
import math
import polygonNode
import polygon
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class pursuitStrategy():
	criticalBeam = QLineF()
	vertices = []
	pursuerCoord = QPointF()
	evaderCoord = QPointF()
	poly = polygon.polygon(vertices)
	beams = []
	hCuts = []
	beamGraph = []
	hGraph = []
	
	def __init__(self, pCoord=QPointF(), eCoord=QPointF(), p=polygon.polygon(vertices), b=[], h=[]):
		self.pursuerCoord = pCoord
		self.evaderCoord = eCoord
		self.poly = p
		self.beams = b
		self.hCuts = h
		self.initiateBeamGraph()
		self.initiateHGraph()
		self.setCriticalBeam()
		
	def sortByXValue(self, lines):
		xValues = []
		temp = []
		for line in lines:
			xValues.append(line.p1().x())
			temp.append(line)
		xValues = sorted(xValues)
		for i in range(len(temp)):
			lines[xValues.index(temp[i].p1().x())] = temp[i]
			xValues[xValues.index(temp[i].p1().x())] = -1
		
	def sortByYValue(self, lines):
		yValues = []
		temp = []
		for line in lines:
			yValues.append(line.p1().y())
			temp.append(line)
		yValues = sorted(yValues)
		for i in range(len(temp)):
			lines[yValues.index(temp[i].p1().y())] = temp[i]
			yValues[yValues.index(temp[i].p1().y())] = -1
			
	def getExtendedBeam(self, beam):
		extBeam = QLineF(beam.p1(), beam.p2())
		for i in range(len(self.beams)):
			if extBeam.p1().x() == self.beams[i].p1().x():
				if extBeam.p1() == self.beams[i].p2():
					extBeam = QLineF(self.beams[i].p1(),extBeam.p2())
				if extBeam.p2() == self.beams[i].p1():
					extBeam = QLineF(extBeam.p1(), self.beams[i].p2())
		return extBeam
		
	def getExtendedHCut(self, hCut):
		extCut = QLineF(hCut.p1(), hCut.p2())
		for i in range(len(self.hCuts)):
			if extCut.p1().y() == self.hCuts[i].p1().y():
				if extCut.p1() == self.hCuts[i].p2():
					extCut = QLineF(self.hCuts[i].p1(),extCut.p2())
				if extCut.p2() == self.hCuts[i].p1():
					extCut = QLineF(extCut.p1(), self.hCuts[i].p2())
		return extCut
		
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
		
	def distance(self, point1, point2):
		line = QLineF(point1, point2)
		return line.length()
			
	def getFirstIntersectingBeam(self, edge, vertex, originalBeam):
		intersectingBeam = QLineF()
		intersectionPoint = QPointF()
		if not vertex == edge.p2():
			shortestDist = self.distance(vertex, edge.p2())
		else:
			shortestDist = self.distance(vertex, edge.p1())
		for beam in self.beams:
			if self.beamIntersectsWithEdge(beam, edge, intersectionPoint):
				dist = self.distance(intersectionPoint, vertex)
				if not (round(vertex.x(),3) == round(intersectionPoint.x(),3) and round(vertex.y(),3) == round(intersectionPoint.y(),3)) and dist <= shortestDist:
					intersectingBeam = beam
					shortestDist = dist
		return intersectingBeam
		
	def getFirstIntersectingHCut(self, edge, vertex, originalHCut):
		intersectingCut = QLineF()
		intersectionPoint = QPointF()
		if not vertex == edge.p2():
			shortestDist = self.distance(vertex, edge.p2())
		else:
			shortestDist = self.distance(vertex, edge.p1())
		for hCut in self.hCuts:
			if self.hCutIntersectsWithEdge(hCut, edge, intersectionPoint):
				dist = self.distance(intersectionPoint, vertex)
				if not (round(vertex.x(),3) == round(intersectionPoint.x(),3) and round(vertex.y(),3) == round(intersectionPoint.y(),3)) and dist <= shortestDist:
					intersectingCut = hCut
					shortestDist = dist
		return intersectingCut
			
	def findCounterclockwiseSubpolygonFromBeam(self, beam):
		verts = []
		intersectionPoint = QPointF()
		edge = self.poly.edgeFromBeamIntersectionPoint(beam, beam.p1(), 0, 1)
		verts.append(edge.p1())
		startingVertex = self.poly.getVertices().index(edge.p2())
		intersectionBeam = self.getFirstIntersectingBeam(edge, edge.p1(), beam)
		if intersectionBeam:
			extBeam = self.getExtendedBeam(intersectionBeam)
			if self.poly.pointsRight(intersectionBeam, extBeam):
				intersectionBeam = extBeam
			verts.append(intersectionBeam.p1())
			verts.append(intersectionBeam.p2())
		else:
			for i in range(startingVertex, len(self.poly.getVertices())):
				verts.append(self.poly.getVertices()[i])
				currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i+1])
				intersectionBeam = self.getFirstIntersectingBeam(currentEdge, self.poly.getVertices()[i], beam)
				if intersectionBeam:
					extBeam = self.getExtendedBeam(intersectionBeam)
					if self.poly.pointsRight(intersectionBeam, extBeam):
						intersectionBeam = extBeam
					if round(intersectionBeam.p2().x(),3) == round(beam.p2().x(),3) or round(intersectionBeam.p1().x(),3) == round(beam.p1().x(),3):
						verts.append(beam.p2())
						verts.append(beam.p1())
						return verts
					verts.append(intersectionBeam.p1())
					verts.append(intersectionBeam.p2())
					break
				if i == len(self.poly.getVertices())-2:
					i = 0
		edge2 = self.poly.edgeFromBeamIntersectionPoint(intersectionBeam, intersectionBeam.p2(), 1, 1)
		if edge2.intersect(beam, intersectionPoint) == QLineF.BoundedIntersection:
			verts.append(intersectionPoint)
			verts.append(beam.p1())
			return verts
		startingVertexForLowerVertices = self.poly.getVertices().index(edge2.p2())
		for i in range(startingVertexForLowerVertices, len(self.poly.getVertices())-1):
			verts.append(self.poly.getVertices()[i])
			currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i+1])
			if currentEdge.intersect(beam, intersectionPoint) == QLineF.BoundedIntersection:
				verts.append(intersectionPoint)
				verts.append(beam.p1())
				return verts
			if i > len(self.poly.getVertices())-3:
				i = 0
		return verts
		
	def findCounterclockwiseSubpolygonFromHCut(self, hCut):
		verts = []
		intersectionPoint = QPointF()
		edge = self.poly.edgeFromHCutIntersectionPoint(hCut, hCut.p1(), 0, 1)
		verts.append(edge.p1())
		startingVertex = self.poly.getVertices().index(edge.p2())
		intersectionCut = self.getFirstIntersectingHCut(edge, edge.p1(), hCut)
		if intersectionCut:
			"Found intersection on first edge"
			extCut = self.getExtendedHCut(intersectionCut)
			if self.poly.pointsUp(intersectionCut, extCut):
				intersectionCut = extCut
			verts.append(intersectionCut.p1())
			verts.append(intersectionCut.p2())
		else:
			for i in range(startingVertex, len(self.poly.getVertices())):
				verts.append(self.poly.getVertices()[i])
				currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i+1])
				intersectionCut = self.getFirstIntersectingHCut(currentEdge, self.poly.getVertices()[i], hCut)
				if intersectionCut:
					extCut = self.getExtendedHCut(intersectionCut)
					if self.poly.pointsUp(intersectionCut, extCut):
						intersectionCut = extCut
					if intersectionCut.p2() == hCut.p2() or intersectionCut.p1() == hCut.p1():
						verts.append(hCut.p2())
						verts.append(hCut.p1())
						return verts
					verts.append(intersectionCut.p1())
					verts.append(intersectionCut.p2())
					break
				elif self.hCutIntersectsWithEdge(hCut, currentEdge, intersectionPoint):
					verts.append(intersectionPoint)
					verts.append(hCut.p1())
					return verts
				if i == len(self.poly.getVertices())-2:
					i = 0
		edge2 = self.poly.edgeFromHCutIntersectionPoint(intersectionCut, intersectionCut.p2(), 1, 1)
		if edge2.intersect(hCut, intersectionPoint) == QLineF.BoundedIntersection:
			verts.append(intersectionPoint)
			verts.append(hCut.p1())
			return verts
		startingVertexForLowerVertices = self.poly.getVertices().index(edge2.p2())
		for i in range(startingVertexForLowerVertices, len(self.poly.getVertices())-1):
			verts.append(self.poly.getVertices()[i])
			currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i+1])
			if currentEdge.intersect(hCut, intersectionPoint) == QLineF.BoundedIntersection:
				verts.append(intersectionPoint)
				verts.append(hCut.p1())
				return verts
			if i > len(self.poly.getVertices())-3:
				i = 0
		return verts
					
	def findClockwiseSubpolygonFromBeam(self, beam):
		verts = []
		intersectionPoint = QPointF()
		edge = self.poly.edgeFromBeamIntersectionPoint(beam, beam.p1(), 1, 0)
		verts.append(edge.p1())
		startingVertex = self.poly.getVertices().index(edge.p2())
		intersectionBeam = self.getFirstIntersectingBeam(edge, edge.p1(), beam)
		if intersectionBeam:
			return []
		else:
			for i in range(startingVertex, -1, -1):
				verts.append(self.poly.getVertices()[i])
				currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i-1])
				intersectionBeam = self.getFirstIntersectingBeam(currentEdge, self.poly.getVertices()[i], beam)
				if intersectionBeam and not self.getExtendedBeam(intersectionBeam) == self.getExtendedBeam(beam):
						return []
				verts.append(beam.p2())
				verts.append(beam.p1())
				return verts
				if i < 1:
					i = len(self.poly.getVertices()-1)
		return verts
		
	def findClockwiseSubpolygonFromHCut(self, hCut):
		verts = []
		intersectionPoint = QPointF()
		edge = self.poly.edgeFromHCutIntersectionPoint(hCut, hCut.p1(), 1, 0)
		verts.append(edge.p1())
		startingVertex = self.poly.getVertices().index(edge.p2())
		intersectionCut = self.getFirstIntersectingHCut(edge, edge.p1(), hCut)
		if intersectionCut:
			return []
		else:
			for i in range(startingVertex, -1, -1):
				verts.append(self.poly.getVertices()[i])
				currentEdge = QLineF(self.poly.getVertices()[i], self.poly.getVertices()[i-1])
				intersectionCut = self.getFirstIntersectingHCut(currentEdge, self.poly.getVertices()[i], hCut)
				if intersectionCut and not self.getExtendedHCut(intersectionCut) == self.getExtendedHCut(hCut):
						return []
				verts.append(hCut.p2())
				verts.append(hCut.p1())
				return verts
				if i < 2:
					i = len(self.poly.getVertices()-1)
		return verts
	
	def initiateBeamGraph(self):
		self.sortByXValue(self.beams)
		for i in range(len(self.beams)):
			beamCellCCW = polygonNode.polygonNode()
			beamCellCW = polygonNode.polygonNode()
			ccwVerts = []
			cwVerts = []
			extBeam = self.getExtendedBeam(self.beams[i])
			if extBeam == self.beams[i]:
				ccwVerts = self.findCounterclockwiseSubpolygonFromBeam(self.beams[i])
				cwVerts = self.findClockwiseSubpolygonFromBeam(self.beams[i])
			else:
				if self.poly.pointsRight(self.beams[i], extBeam):
					ccwVerts = self.findCounterclockwiseSubpolygonFromBeam(self.beams[i])
					if extBeam.p1() == self.beams[i].p1():
						cwVerts = self.findClockwiseSubpolygonFromBeam(extBeam)
				else:
					cwVerts = self.findClockwiseSubpolygonFromBeam(self.beams[i])
					if extBeam.p1() == self.beams[i].p1():
						ccwVerts = self.findCounterclockwiseSubpolygonFromBeam(extBeam)
			if len(ccwVerts) > 0:
				beamCellCCW.setPolygon(ccwVerts)
				print "beam cell ccw:",
				print beamCellCCW.getPolygon().getVertices()
				self.beamGraph.append(beamCellCCW)
			if len(cwVerts) > 0:
				beamCellCW.setPolygon(cwVerts)
				print "beam cell cw:",
				print beamCellCW.getPolygon().getVertices()
				self.beamGraph.append(beamCellCW)
					
	def initiateHGraph(self):
		self.sortByYValue(self.hCuts)
		for i in range(len(self.hCuts)):
			hCellCCW = polygonNode.polygonNode()
			hCellCW = polygonNode.polygonNode()
			ccwVerts = []
			cwVerts = []
			extCut = self.getExtendedHCut(self.hCuts[i])
			if extCut == self.hCuts[i]:
				ccwVerts = self.findCounterclockwiseSubpolygonFromHCut(self.hCuts[i])
				cwVerts = self.findClockwiseSubpolygonFromHCut(self.hCuts[i])
			else:
				if self.poly.pointsUp(self.hCuts[i], extCut):
					ccwVerts = self.findCounterclockwiseSubpolygonFromHCut(self.hCuts[i])
					if extCut.p1() == self.hCuts[i].p1():
						cwVerts = self.findClockwiseSubpolygonFromHCut(extCut)
				else:
					cwVerts = self.findClockwiseSubpolygonFromHCut(self.hCuts[i])
					if extCut.p1() == self.hCuts[i].p1():
						ccwVerts = self.findCounterclockwiseSubpolygonFromHCut(extCut)
			if len(ccwVerts) > 0:
				hCellCCW.setPolygon(ccwVerts)
				print "h cell ccw:",
				print hCellCCW.getPolygon().getVertices()
				self.hGraph.append(hCellCCW)
			if len(cwVerts) > 0:
				hCellCW.setPolygon(cwVerts)
				print "h cell cw:",
				print hCellCW.getPolygon().getVertices()
				self.hGraph.append(hCellCW)
			
	def getCriticalBeam(self):
		return self.criticalBeam
			
	def setCriticalBeam(self):
		pursuerCell = polygonNode.polygonNode()
		for cell in self.hGraph:
			if cell.hasPursuer(self.pursuerCoord):
				pursuerCell = cell
		for beam in self.beams:
			if beam.p1().x() >= self.evaderCoord.x() and beam.p1().x() <= self.pursuerCoord.x() or beam.p1().x() <= self.evaderCoord.x() and beam.p1().x() >= self.pursuerCoord.x():
				extBeam = self.getExtendedBeam(beam)
				if self.beamIntersectsWithEdge(self.getExtendedBeam(beam), QLineF(pursuerCell.getPolygon().getVertices()[0], pursuerCell.getPolygon().getVertices()[len(pursuerCell.getPolygon().getVertices())-2]), QPointF()):
					print extBeam
					self.criticalBeam = extBeam
	
	def getNumPursuers(self):
		return
	
	def getPursuerCoord(pursuer):
		return
			
	def getEvaderCoord(self):
		return
		
	def advanceEvader(self):
		return
	
	def advancePursuer(self):
		return