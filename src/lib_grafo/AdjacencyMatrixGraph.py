from TpPraticoGrafos.src.lib_grafo.AbstractGraph import AbstractGraph

class AdjacencyMatrixGraph(AbstractGraph):

    def __init__(self, numVertices: int):
        self.numVertices = numVertices
        self.numArestas = 0
        self.matrix = [[0 for _ in range(numVertices)] for _ in range(numVertices)]


    def getVertexCount(self) -> int:
        return self.numVertices

    def getEdgeCount(self) -> int:
        return self.numArestas

    def validVertex(self, v: int):
        if v > self.numVertices or v <= 0:
            raise ValueError("Índice de vértice inválido")

    def hasEdge(self, v: int, w: int) -> bool:
        self.validVertex(v)
        self.validVertex(w)

        row = v - 1
        col = w - 1

        if self.matrix[row][col] == 0 | self.matrix[col][row] == 0:
            return False
        return True

    def addEdge(self, v: int, w: int):
        self.validVertex(v)
        self.validVertex(w)
        if v == w:
            raise ValueError("Não é possível adicionar arestar que gerem laços.")
        row = v - 1
        col = w - 1

        #if self.isDivergent(v, w):
            #raise ValueError("Aresta existente")
        self.matrix[row][col] = 1
        self.numArestas += 1

    def removeEdge(self, v: int, w: int):
        self.validVertex(v)
        self.validVertex(w)

        if self.hasEdge(v, w):
            row = v - 1
            col = w - 1
            self.matrix[row][col] = 0
            self.numArestas -= 1
        else:
            raise ValueError("Não existe aresta para remover")

    def isSuccessor(self, suc: int, pre: int):
        self.validVertex(suc)
        self.validVertex(pre)
        if self.hasEdge(pre, suc):
            return True
        return False

    def isPredecessor(self, pre: int, suc: int):
        self.validVertex(pre)
        self.validVertex(suc)
        if self.hasEdge(pre, suc):
            return True
        return False

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:

        return (u1 == u2) and (v1 != v2) and self.hasEdge(u1, v1) and self.hasEdge(u2, v2)
    def isConvergent(self):
        pass
    def isIncident(self, v: int, w: int, x: int):
        pass

    def getVertexInDegree(self, u: int):
        self.validVertex(u)
        degree = 0

        for row in self.matrix:
            if row[u-1] == 1:
                degree += 1
        return degree

    def getVertexOutDegree(self, u: int):
        self.validVertex(u)
        degree = 0

        for col in self.matrix[u - 1]:
            if col == 1:
                degree += 1
        return degree

    def isIncident(self, u: int,v: int, x: int) -> bool:
        pass
        #self.validVertex(u)
        #self.validVertex(v)
        #self.validVertex(x)

        #if self.hasEdge(u, v):
         #   if u == x:

    def setVertexWeight(self, v: int, w: float):
        pass

    def setEdgeWeight(self, u: int, v: int, w: float):
        self.validVertex(u)
        self.validVertex(v)
        row = u -1
        col = v -1

        if self.hasEdge(u, v):
            self.matrix[row][col] = w
        else:
            raise ValueError("Não existe aresta para adicionar peso")

    def getEdgeWeight(self, u: int, v: int) -> float:
        self.validVertex(u)
        self.validVertex(v)
        row = u - 1
        col = v - 1

        if self.hasEdge(u, v):
            return float(self.matrix[row][col])
        else:
            raise ValueError("Não existe aresta entre os vertices.")

    def isconnected(self) -> bool:
        if self.numVertices == 0:
            return True

        # declara todos os vértices como não visitados
        undirected_visited = [False] * self.numVertices

        # chama a busca, iniciando do vertice 1 (nosso primeiro)
        self.buscaEmProfundidade(1, undirected_visited)

        # Verifica se visitou todos os vértices
        return all(undirected_visited)

    def buscaEmProfundidade(self, v: int, visited: list[bool]):
        v_index = v - 1

        visited[v_index] = True

        for neighbor_index in range(self.numVertices):
            # Se existe aresta de v_index para neighbor_index OU de neighbor_index para v_index
            if (self.matrix[v_index][neighbor_index] != 0 or self.matrix[neighbor_index][v_index] != 0):

                # Se o vizinho (pelo seu índice 0-base) ainda não foi visitado
                if not visited[neighbor_index]:
                    # como o index é inicializado em 0 para passear pela matriz, é necessário adicionar 1, para ficar o id correto
                    neighbor_id = neighbor_index + 1
                    self.buscaEmProfundidade(neighbor_id, visited)

    def isEmptyGraph(self) -> bool:
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                if self.matrix[i][j] != 0:
                    return False

        return True

    def isCompleteGraph(self) -> bool:
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                if i != j:
                    if self.matrix[i][j] == 0:
                        return False
        return True

