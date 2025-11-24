from src.lib_grafo.AbstractGraph import AbstractGraph

class AdjacencyListGraph(AbstractGraph):

    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.adjacencias = {i: [] for i in range(numVertices)}
        self.edge_weights = {}
        self.vertex_weights = {}

    def _validate_vertex(self, v):
        if v < 0 or v >= self.numVertices:
            raise IndexError(f"Vertice {v} invalido")

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
        self._validate_vertex(u)
        self._validate_vertex(v)

        for i in range(len(self.adjacencias[u])):
            if self.adjacencias[u][i] == v:
                return True
        return False

    def addEdge(self, u: int, v: int):
        self._validate_vertex(u)
        self._validate_vertex(v)

        if v == u:
            return
        if self.hasEdge(u, v):
            return

        self.adjacencias[u].append(v)

    def removeEdge(self, u: int, v: int):
        self._validate_vertex(u)
        self._validate_vertex(v)

        if self.hasEdge(u, v):
            self.adjacencias[u].remove(v)
        else:
            raise ValueError("aresta nao existe")

    def isSucessor(self, u: int, v: int) -> bool:
        self._validate_vertex(u)
        self._validate_vertex(v)

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
        self._validate_vertex(u)

        grau = 0
        for i in range(self.numVertices):
            for j in range(len(self.adjacencias[i])):
                if self.adjacencias[i][j] == u:
                    grau += 1
        return grau

    def getVertexOutDegree(self, u: int):
        self._validate_vertex(u)

        grau = 0
        for i in range(len(self.adjacencias[u])):
            grau += 1
        return grau

    def setVertexWeight(self, v: int, w: float):
        self._validate_vertex(v)

        self.vertex_weights[v] = w

    def getVertexWeight(self, v: int):
        self._validate_vertex(v)

        return self.vertex_weights[v]

    def setEdgeWeight(self, u: int, v: int, w: float):
        # haxEdge ja trata exceções, verificando o U e V
        if not self.hasEdge(u, v):
            raise ValueError("aresta nao existe para definir peso")
        self.edge_weights[(u, v)] = w

    def getEdgeWeight(self, u: int, v: int):
        return self.edge_weights.get((u, v))

    def isCompleteGraph(self) -> bool:
        return self.getEdgeCount() == (self.getVertexCount() * (self.getVertexCount() - 1))

    def isEmptyGraph(self) -> bool:
        return self.getEdgeCount() == 0

    def isConnected(self) -> bool:
        if self.numVertices == 0:
            return True

        # marca todos os V como não visitados
        visited = [False] * self.numVertices

        # chama a busca em profundidade começando do V = 0
        self.buscaProfundidade(0, visited)

        # caso todas os V estiverem marcado como visitado volta TRUE
        return all(visited)

    def buscaProfundidade(self, v: int, visited: list[bool]):
        visited[v] = True

        # laço visitando todos os vizinhos diretos (arestas v -> x)
        for neighbor in self.adjacencias[v]:
            if not visited[neighbor]:
                self.buscaProfundidade(neighbor, visited)

        # procura todos os vertices que tem "v" como sucessor (arestas x -> v)
        for u in range(self.numVertices):
            if v in self.adjacencias[u] and not visited[u]:
                self.buscaProfundidade(u, visited)

    def mostrarGrafo(self):
        for u, vizinhos in self.adjacencias.items():
            print(f"{u} -> {vizinhos}")

    def exportToGEPHI(self, path: str):
        import xml.etree.ElementTree as ET
        gexf = ET.Element("gexf", {
            "xmlns": "http://www.gexf.net/1.2draft",
            "version": "1.2"
        })
        graph = ET.SubElement(gexf, "graph", {
            "mode": "static",
            "defaultedgetype": "directed"
        })
        nodes = ET.SubElement(graph, "nodes")

        for u in range(self.numVertices):
            peso_vertice = self.vertex_weights.get(u, 0)

            ET.SubElement(nodes, "node", {
                "id": str(u + 1),
                "label": f"V{u + 1}",
                "weight": str(peso_vertice)
            })

        edges = ET.SubElement(graph, "edges")
        edge_id = 0

        for u in range(self.numVertices):
            for v in self.adjacencias[u]:
                peso_aresta = self.edge_weights.get((u, v), 0)

                ET.SubElement(edges, "edge", {
                    "id": str(edge_id),
                    "source": str(u + 1),
                    "target": str(v + 1),
                    "weight": str(peso_aresta)
                })

                edge_id += 1
        tree = ET.ElementTree(gexf)
        tree.write(path, encoding="utf-8", xml_declaration=True)

        print(f"Grafo exportado com sucesso para: {path}")

