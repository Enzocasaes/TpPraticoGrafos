import os
import vertice
from collections import deque
import AbstractGraph

from src.lib_grafo.aresta import aresta


class AdjacencyListGraph:


    def init(self, num_vertices):
        super().init(num_vertices)
        self.adjacencias = {i: [] for i in range(num_vertices)}
        self.edge_weights = {}


    def getVertexCount(self):
        return self.num_vertices


    def getEdgeCount(self):
        int totalArestas = 0
        for i in range(self.num_vertices):
            for j in range(len(self.adjacencias[i])):
                if self.adjacencias[i][j] is not None:
                    totalArestas += 1
        return totalArestas


    def hasEdge(self, u: int, v: int) -> bool:
              for i in range(len(self.adjacencias[u])):
                  if self.adjacencias[u][i] == v:
                      return True
              return False


    def addEdge(self, u: int, v: int):
        if self.isSucessor(self, u, v) or v == u:
           print("ja possui esta aresta")
           pass
        self.adjacencias[u].append(v)


    def removeEdge(self, u: int, v: int):
        if self.isSucessor(self, u, v):
            self.adjacencias[u].remove(v)
        else:
            print("aresta nao existe")



    def isSucessor(self, u: int, v: int)-> bool:
        for i in range(len(self.adjacencias[u])):
            if self.adjacencias[u][i] == v:
                return True
        return False


    def isPredecessor(self, u: int, v: int) -> bool:
        return self.isSucessor(self, v, u)


    def isDivergent(self, u1: int, v1: int, u2: int, v2: int):
                pass

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int):
                pass

    def isIncident(self, u: int, v1: int, u2: int, v2: int):
                pass

    def getVertexInDegree(self, u: int):
        int grau = 0
        for i in range(self.num_vertices):
            for j in range(len(self.adjacencias[i])):
                if self.adjacencias[i][j] == u:
                    grau += 1
        return grau

    def getVertexOutDegree(self, u: int):
        int grau = 0
        for i in range(len(self.adjacencias[u])):
            grau += 1
        return grau

    def setVertexWeight(self, v: int, w: float):
                pass

    def getVertexWeight(self, v: int):
                pass

    def setEdgeWeight(self, v: int, u: int, w: float):
                pass

    def getEdgeWeight(self, u: int, v: int):
                pass

    def isConnected(self):
                pass

    def isEmptyGraph(self) -> bool:
        if(self.getEdgeCount() == 0):
            return True
        return False

    def isCompleteGraph(self) -> bool:
        if self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1)):
            return True
        return False






