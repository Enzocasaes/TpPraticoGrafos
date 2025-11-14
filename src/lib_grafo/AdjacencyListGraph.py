import os
#import vertice
from collections import deque
from src.lib_grafo.AbstractGraph import AbstractGraph

#from src.lib_grafo.aresta import aresta


class AdjacencyListGraph:


    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.adjacencias = {i: [] for i in range(numVertices)}
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
            print(f"ja possui esta aresta: {u} -> {v} ")
            return
        if self.hasEdge(v, u):
            print(f"antiparalela: {u} -> {v} ")
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

    def isCompleteGraph(self) -> bool:
        return self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1))

    def isEmptyGraph(self) -> bool:
        return self.getEdgeCount() == 0

    def mostrarGrafo(self):
        for u, vizinhos in self.adjacencias.items():
            print(f"{u} -> {vizinhos}")

# --- Teste simples da inicialização ---
os.system('cls' if os.name == 'nt' else 'clear')

numVertices = int(input("Digite o número de vértices: "))
graph = AdjacencyListGraph(numVertices)

print("\nMatriz de Adjacência Inicial:")
# Vértice 1 se conecta a todos os outros
graph.addEdge(1, 2)
graph.addEdge(1, 3)
graph.addEdge(1, 4)

# Vértice 2 se conecta a todos os outros
graph.addEdge(2, 1)
graph.addEdge(2, 3)
graph.addEdge(2, 4)

# Vértice 3 se conecta a todos os outros
graph.addEdge(3, 1)
graph.addEdge(3, 2)
graph.addEdge(3, 4)

# Vértice 4 se conecta a todos os outros
graph.addEdge(4, 1)
graph.addEdge(4, 2)
graph.addEdge(4, 3)
graph.setEdgeWeight(1,2,5)
graph.setEdgeWeight(2,4,9)
print(len())
#print(graph.isCompleteGraph())
#print(graph.getVertexInDegree(1))
#print(graph.getVertexInDegree(4))
#print(graph.getVertexOutDegree(1))
#print(graph.getVertexOutDegree(4))
#print(graph.isSucessor(3, 1))
#print(graph.isSucessor(4, 3))
#print(graph.isPredecessor(3, 1))
#print(graph.getVertexCount())
#print(graph.getEdgeCount())
#print(graph.hasEdge(1, 2))
#print(graph.hasEdge(2, 1))
#print(graph.hasEdge(1, 3))
