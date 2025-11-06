import os

class AdjacencyMatrixGraph:

    def __init__(self, numVertices: int):
        self.numVertices = numVertices
        self.numArestas = 0
        ### Inicializa uma matrix de Vértice X Vértice
        self.matrix = [[0 for _ in range(numVertices)] for _ in range(numVertices)]


    def getVertexCount(self) -> int:
        return self.numVertices

    def getEdgeCount(self) -> int:
        return self.numArestas

    def validVertex(self, v: int):
        if v >= self.numVertices or v < 0:
            raise ValueError("Índice de vértice inválido")

    def hasEdge(self, v: int, w: int) -> bool:
        row = v - 1
        col = w - 1

        self.validVertex(row)
        self.validVertex(col)

        if self.matrix[row][col] == 0:
            return False
        return True

    def addEdge(self, v: int, w: int):
        row = v - 1
        col = w - 1

        self.validVertex(row)
        self.validVertex(col)

        if self.hasEdge(v, w):
            raise ValueError("Aresta existente")
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
        if self.hasEdge(pre, suc):
            return True
        return False

    def isPredecessor(self, pre: int, suc: int):
        if self.hasEdge(pre, suc):
            return True
        return False

    ##def isDivergent(self):
    ##def isConvergent(self):
    ##def isIncident(self, v: int, w: int, x: int):

    def getVertexInDegree(self, u: int):
        self.validVertex(u-1)
        degree = 0

        for row in self.matrix:
            if row[u-1] == 1:
                degree += 1
        return degree

    def getVertexOutDegree(self, u: int):
        self.validVertex(u-1)
        degree = 0

        for col in self.matrix[u - 1]:
            if col == 1:
                degree += 1
        return degree



# --- Teste simples da inicialização ---
os.system('cls' if os.name == 'nt' else 'clear')

num_vertices = int(input("Digite o número de vértices: "))
graph = AdjacencyMatrixGraph(num_vertices)

print("\nMatriz de Adjacência Inicial:")
graph.addEdge(1, 2)
graph.addEdge(1, 3)
graph.addEdge(2, 4)
graph.addEdge(3, 4)
##print(graph.getVertexInDegree(1))
##print(graph.getVertexInDegree(4))
print(graph.getVertexOutDegree(1))
print(graph.getVertexOutDegree(4))
# print(graph.isSuccessor(3, 1))
# print(graph.isSuccessor(4, 3))
# print(graph.isPredecessor(1, 3))
# print(graph.getVertexCount())
# print(graph.getEdgeCount())
# print(graph.hasEdge(1, 2))
# print(graph.hasEdge(3, 1))
# print(graph.hasEdge(1, 3))
for i in range(graph.numVertices + 1):
    # Primeira linha (cabeçalho)
    if i == 0:
        print("   ", end="")
        for j in range(graph.numVertices):
            print(f"{j:3}", end="")
        print()
    else:
        # Linha da matriz com índice da linha
        print(f"{i-1:2} ", end="")
        for j in range(graph.numVertices):
            print(f"{graph.matrix[i-1][j]:3}", end="")
        print()
print()
# graph.removeEdge(3, 1)
# for i in range(graph.numVertices + 1):
#     # Primeira linha (cabeçalho)
#     if i == 0:
#         print("   ", end="")
#         for j in range(graph.numVertices):
#             print(f"{j:3}", end="")
#         print()
#     else:
#         # Linha da matriz com índice da linha
#         print(f"{i-1:2} ", end="")
#         for j in range(graph.numVertices):
#             print(f"{graph.matrix[i-1][j]:3}", end="")
#         print()
# print()