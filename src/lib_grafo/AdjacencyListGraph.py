import os
import vertice
from collections import deque
import AbstractGraph

from src.lib_grafo.aresta import aresta


class AdjacencyListGraph:

    def __init__(self, num_vertices: int):
        self.numVertices = num_vertices
        self.adjacencias = {i: [] for i in range(num_vertices)}
        self.edge_weights = {}
        self.vertex_weights = {}



    def getVertexCount(self):
        return self.numVertices

    def getEdgeCount(self):
        total = 0
        for u in self.adjacencias:
            total += len(self.adjacencias[u])
        return total

    #def getEdgeCount(self):
        #int totalArestas = 0
        #for i in range(self.num_vertices):
         #   for j in range(len(self.adjacencias[i])):
        #        if self.adjacencias[i][j] is not None:
         #           totalArestas += 1
        #return totalArestas

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
        try:
            weight = float(w)
        except (TypeError, ValueError):
            raise ValueError('Peso inválido; espere um número.')
        self.vertex_weights[v] = weight

    def getVertexWeight(self, v: int):
        return self.vertex_weights.get(v, 0.0)

    def setEdgeWeight(self, u: int, v: int, w: float):
        try:
            weight = float(w)
        except (TypeError, ValueError):
            raise ValueError('Peso inválido; espere um número.')

        self.edge_weights[(u, v)] = weight

    def getEdgeWeight(self, u: int, v: int):
        return self.edge_weights.get((u, v), 0.0)

    def isConnected(self):
       
        # Busca em largura
        visited = [False] * n
        q = deque([0])
        visited[0] = True
        while q:
            u = q.popleft() # remove e retorna o elemento mais à esquerda 
            for v in self.adjacencias.get(u, []):
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

        if not all(visited):
            return False

        # constroi grafo transposto
        rev = {i: [] for i in range(n)}
        for u in range(n):
            for v in self.adjacencias.get(u, []):
                rev[v].append(u)

        visited = [False] * n
        q = deque([0])
        visited[0] = True
        while q:
            u = q.popleft()
            for v in rev.get(u, []):
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

        return all(visited)

    def isEmptyGraph(self) -> bool:
        if(self.getEdgeCount() == 0):
            return True
        return False

    def isCompleteGraph(self) -> bool:
        if self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1)):
            return True
        return False






