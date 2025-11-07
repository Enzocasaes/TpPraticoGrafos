import os
from collections import deque
from src.lib_grafo.AbstractGraph import AbstractGraph

class AdjacencyListGraph(AbstractGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self.adjacencias = {i: [] for i in range(num_vertices)}
        self.edge_weights = {}
        self.vertex_weights = {}

    def getVertexCount(self):
        return self.numVertices

    def getEdgeCount(self):
        totalArestas = 0
        for i in range(self.numVertices):
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
        if v == u:
            print("nao e permitido laco")
            return
        if self.hasEdge(u, v):
            print("ja possui esta aresta")
            return
        self.adjacencias[u].append(v)

    def removeEdge(self, u: int, v: int):
        if self.hasEdge(u, v):
            self.adjacencias[u].remove(v)
        else:
            print("aresta nao existe")

    def isSucessor(self, u: int, v: int) -> bool:
        for i in range(len(self.adjacencias[u])):
            if self.adjacencias[u][i] == v:
                return True
        return False

    def isPredecessor(self, u: int, v: int) -> bool:
        return self.isSucessor(v, u)

    def isDivergent(self, u1, v1, u2, v2):
        return u1 == u2 and (v1 != v2)

    def isConvergent(self, u1, v1, u2, v2):
        return v1 == v2 and (u1 != u2)

    def isIncident(self, u, v, x):
        return x == u or x == v

    def getVertexInDegree(self, u: int):
        grau = 0
        for i in range(self.numVertices):
            for j in range(len(self.adjacencias[i])):
                if self.adjacencias[i][j] == u:
                    grau += 1
        return grau

    def getVertexOutDegree(self, u: int):
        grau = 0
        for i in range(len(self.adjacencias[u])):
            grau += 1
        return grau

    def setVertexWeight(self, v: int, w: float):
        self.vertex_weights[v] = w

    def getVertexWeight(self, v: int):
        return self.vertex_weights[v]

    def setEdgeWeight(self, u: int, v: int, w: float):
        if not self.hasEdge(u, v):
            raise ValueError("aresta nao existe para definir peso")
        self.edge_weights[(u, v)] = w

    def getEdgeWeight(self, u: int, v: int):
        return self.edge_weights.get((u, v), 1.0)

    def isConnected(self):
        visitados = set()
        def dfs(v):
            if v not in visitados:
                visitados.add(v)
                for viz in self.adjacencias[v]:
                    dfs(viz)
        dfs(0)
        return len(visitados) == self.numVertices

    def isEmptyGraph(self) -> bool:
        return self.getEdgeCount() == 0

    def isCompleteGraph(self) -> bool:
        return self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1))

    def mostrarGrafo(self):
        for u, vizinhos in self.adjacencias.items():
            print(f"{u} -> {vizinhos}")
