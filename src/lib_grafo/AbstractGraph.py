from abc import ABC, abstractmethod

class AbstractGraph(ABC):

    def __init__(self, numVertices:int):
        self.numVertices = numVertices
        self.numEdges = 0

    @abstractmethod
    def getVertexCount(self):
        pass

    @abstractmethod
    def getEdgeCount(self):
        pass

    @abstractmethod
    def hasEdge(self, u:int, v:int):
        pass

    @abstractmethod
    def addEdge(self, u:int, v:int):
        pass

    @abstractmethod
    def removeEdge(self, u:int, v:int):
        pass

    @abstractmethod
    def isSucessor(self, u:int, v:int):
        pass

    @abstractmethod
    def isPredecessor(self, u:int, v:int):
        pass

    @abstractmethod
    def isDivergent(self, u1:int, v1:int, u2:int, v2:int):
        pass

    @abstractmethod
    def isConvergent(self, u1:int, v1:int, u2:int, v2:int):
        pass

    @abstractmethod
    def isIncident(self, u:int, v1:int, u2:int, v2:int):
        pass

    @abstractmethod
    def getVertexInDegree(self, u:int):
        pass

    @abstractmethod
    def getVertexOutDegree(self, u:int):
        pass

    @abstractmethod
    def setVertexWeight(self, v:int, w:float):
        pass

    @abstractmethod
    def getVertexWeight(self, v:int):
        pass

    @abstractmethod
    def setEdgeWeight(self, v:int, u:int, w:float):
        pass

    @abstractmethod
    def getEdgeWeight(self, u:int, v:int):
        pass

    @abstractmethod
    def isConnected(self):
        pass

    @abstractmethod
    def isEmptyGraph(self):
        pass

    @abstractmethod
    def isCompleteGraph(self):
        pass

