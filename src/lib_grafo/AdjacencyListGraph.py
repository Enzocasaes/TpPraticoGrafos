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
        return self.edge_weights.get((u, v))

    def isCompleteGraph(self) -> bool:
        return self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1))

    def isEmptyGraph(self) -> bool:
        return self.getEdgeCount() == 0

    def mostrarGrafo(self):
        for u, vizinhos in self.adjacencias.items():
            print(f"{u} -> {vizinhos}")

    def exportToGEPHI(self, path: str):
        """
        Exports the graph to a file in GraphML format (.graphml),
        compatible with the GEPHI visualization software.
        """
        try:
            with open(path, 'w') as f:
                # 1. Write the XML Header and GraphML Root
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" '
                        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                        'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns '
                        'http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')

                # 2. Define Keys for Attributes (Weights)
                # Key for Vertex Weight
                if self.vertex_weights:
                    f.write('  <key id="d0" for="node" attr.name="weight" attr.type="double"/>\n')
                # Key for Edge Weight
                f.write('  <key id="d1" for="edge" attr.name="weight" attr.type="double"/>\n')

                # 3. Start the Graph Structure (directed since you check for antiparallel edges)
                f.write('  <graph id="G" edgedefault="directed">\n')

                # 4. Write Nodes (Vertices)
                for u in range(self.numVertices):
                    f.write(f'    <node id="{u}">\n')
                    # Add Vertex Weight if it exists
                    if u in self.vertex_weights:
                        weight = self.vertex_weights[u]
                        f.write(f'      <data key="d0">{weight}</data>\n')
                    f.write('    </node>\n')

                # 5. Write Edges
                for u in range(self.numVertices):
                    for v in self.adjacencias[u]:
                        edge_key = (u, v)
                        # Get the explicit weight or default to 1.0 (as per getEdgeWeight)
                        weight = self.getEdgeWeight(u, v)

                        f.write(f'    <edge source="{u}" target="{v}">\n')
                        f.write(f'      <data key="d1">{weight}</data>\n')  # Edge weight
                        f.write('    </edge>\n')

                # 6. Close Tags
                f.write('  </graph>\n')
                f.write('</graphml>\n')

            print(f"\nGrafo exportado com sucesso para: {path}")

        except Exception as e:
            print(f"\nErro ao exportar o grafo: {e}")