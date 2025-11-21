import os

from src.lib_grafo.AbstractGraph import AbstractGraph

class AdjacencyMatrixGraph(AbstractGraph):

    def __init__(self, numVertices: int):
        self.numVertices = numVertices
        self.numArestas = 0
        self.matrix = [[(1, 0) for _ in range(numVertices)] for _ in range(numVertices)]


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

        a, peso_aresta_row_col = self.matrix[row][col]
        b, peso_aresta_col_row = self.matrix[col][row]

        if peso_aresta_row_col == 0 and peso_aresta_col_row == 0:
            return False
        return True

    def addEdge(self, v: int, w: int):
        self.validVertex(v)
        self.validVertex(w)
        if v == w:
            raise ValueError("Não é possível adicionar arestar que gerem laços.")
        row = v - 1
        col = w - 1
        peso_vertice, peso_aresta = self.matrix[row][col]

        #if self.isDivergent(v, w):
            #raise ValueError("Aresta existente")
        self.matrix[row][col] = (peso_vertice, 1)
        self.numArestas += 1

    def removeEdge(self, v: int, w: int):
        self.validVertex(v)
        self.validVertex(w)

        if self.hasEdge(v, w):
            row = v - 1
            col = w - 1
            peso_vertice, peso_aresta = self.matrix[row][col]
            self.matrix[row][col] = (peso_vertice, 0)
            self.numArestas -= 1
        else:
            raise ValueError("Não existe aresta para remover")

    def isSucessor(self, suc: int, pre: int) -> bool:
        self.validVertex(suc)
        self.validVertex(pre)

        a, peso_aresta = self.matrix[pre-1][suc-1]
        return peso_aresta != 0

    def isPredecessor(self, pre: int, suc: int) -> bool:
        self.validVertex(pre)
        self.validVertex(suc)

        a, peso_aresta = self.matrix[suc-1][pre-1]
        return peso_aresta != 0

    def isDivergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:

        self.validVertex(u1)
        self.validVertex(v1)
        self.validVertex(u2)
        self.validVertex(v2)
        return (u1 == u2) and (v1 != v2) and self.hasEdge(u1, v1) and self.hasEdge(u2, v2)

    def isConvergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:

        self.validVertex(u1)
        self.validVertex(v1)
        self.validVertex(u2)
        self.validVertex(v2)
        return (v1 == v2) and (u1 != u2) and self.hasEdge(u1, v1) and self.hasEdge(u2, v2)

    def isIncident(self, v: int, w: int, x: int):

        self.hasEdge(v, w)
        return x == v | x == w

    def getVertexInDegree(self, u: int) -> int:
        self.validVertex(u)
        degree = 0

        col = u - 1

        for row in self.matrix:
            _, peso_aresta = row[col]
            if peso_aresta != 0:
                degree += 1

        return degree

    def getVertexOutDegree(self, u: int) -> int:
        self.validVertex(u)
        degree = 0

        for _, peso_aresta in self.matrix[u - 1]:
            if peso_aresta != 0:
                degree += 1

        return degree

    def setVertexWeight(self, v: int, w: float):
        self.validVertex(v)
        index = v - 1  # índice real na matriz (0-based)

        for i in range(len(self.matrix)):
            peso_vertice, peso_aresta = self.matrix[index][i]
            self.matrix[index][i] = (w, peso_aresta)

            peso_vertice, peso_aresta = self.matrix[i][index]
            self.matrix[i][index] = (w, peso_aresta)

    def getVertexWeight(self, v: int):
        self.validVertex(v)
        row = v - 1

        peso_vertice, a = self.matrix[row][row]

        return float(peso_vertice)

    def setEdgeWeight(self, u: int, v: int, w: float):
        self.validVertex(u)
        self.validVertex(v)

        row = u - 1
        col = v - 1

        peso_vertice, peso_aresta = self.matrix[row][col]

        if peso_aresta != 0:
            self.matrix[row][col] = (peso_vertice, w)
        else:
            raise ValueError("Não existe aresta entre os vértices para adicionar peso.")

    def getEdgeWeight(self, u: int, v: int) -> float:
        self.validVertex(u)
        self.validVertex(v)

        row = u - 1
        col = v - 1

        _, peso_aresta = self.matrix[row][col]

        if peso_aresta != 0:
            return float(peso_aresta)
        else:
            raise ValueError("Não existe aresta entre os vértices.")

    def isConnected(self) -> bool:
        if self.numVertices == 0:
            return True

        # declara todos os vértices como não visitados
        undirected_visited = [False] * self.numVertices

        # chama a busca, iniciando do vértice 1 (nosso primeiro)
        self.buscaEmProfundidade(1, undirected_visited)

        # Verifica se visitou todos os vértices
        return all(undirected_visited)

    def buscaEmProfundidade(self, v: int, visited: list[bool]):
        v_index = v - 1
        visited[v_index] = True

        for neighbor_index in range(self.numVertices):
            # obtém o peso da aresta em ambas as direções
            _, peso_aresta_vizinho = self.matrix[v_index][neighbor_index]
            _, peso_aresta_reverso = self.matrix[neighbor_index][v_index]

            # Se existe aresta de v_index → neighbor_index OU neighbor_index → v_index
            if peso_aresta_vizinho != 0 or peso_aresta_reverso != 0:
                # Se o vizinho (pelo seu índice 0-base) ainda não foi visitado
                if not visited[neighbor_index]:
                    # como o index é inicializado em 0 para passear pela matriz, é necessário adicionar 1, para ficar o id correto
                    neighbor_id = neighbor_index + 1
                    self.buscaEmProfundidade(neighbor_id, visited)

    def isEmptyGraph(self) -> bool:
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                _, peso_aresta = self.matrix[i][j]
                if peso_aresta != 0:
                    return False
        return True

    def isCompleteGraph(self) -> bool:
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                if i != j:
                    _, peso_aresta = self.matrix[i][j]
                    if peso_aresta == 0:
                        return False
        return True

    def exportToGEPHI(self, path: str):
        import xml.etree.ElementTree as ET

        # Cria o elemento raiz do grafo
        gexf = ET.Element("gexf", {
            "xmlns": "http://www.gexf.net/1.2draft",
            "version": "1.2"
        })

        # Cria o elemento <graph>
        graph = ET.SubElement(gexf, "graph", {
            "mode": "static",
            "defaultedgetype": "directed"
        })

        # === NODES ===
        nodes = ET.SubElement(graph, "nodes")
        for i in range(self.numVertices):
            peso_vertice, _ = self.matrix[i][i]  # peso do próprio vértice (diagonal)
            ET.SubElement(nodes, "node", {
                "id": str(i + 1),
                "label": f"V{i + 1}",
                "weight": str(peso_vertice)
            })

        # === EDGES ===
        edges = ET.SubElement(graph, "edges")
        edge_id = 0
        for i in range(self.numVertices):
            for j in range(self.numVertices):
                _, peso_aresta = self.matrix[i][j]
                if peso_aresta != 0:
                    ET.SubElement(edges, "edge", {
                        "id": str(edge_id),
                        "source": str(i + 1),
                        "target": str(j + 1),
                        "weight": str(peso_aresta)
                    })
                    edge_id += 1

        # === Escreve o arquivo ===
        tree = ET.ElementTree(gexf)
        tree.write(path, encoding="utf-8", xml_declaration=True)



# --- Teste simples da inicialização ---
os.system('cls' if os.name == 'nt' else 'clear')

num_vertices = int(input("Digite o número de vértices: "))
graph = AdjacencyMatrixGraph(num_vertices)

print("\nMatriz de Adjacência Inicial:")
# Vértice 1 se conecta a todos os outros
#graph.addEdge(1, 2)
#graph.addEdge(1, 3)
#graph.addEdge(1, 4)

# Vértice 2 se conecta a todos os outros
graph.addEdge(2, 1)
graph.addEdge(2, 3)
graph.addEdge(2, 4)

# Vértice 3 se conecta a todos os outros
graph.addEdge(3, 1)
graph.addEdge(3, 2)
graph.addEdge(3, 4)

# Vértice 4 se conecta a todos os outros
#graph.addEdge(4, 1)
#graph.addEdge(4, 2)
#graph.addEdge(4, 3)
# graph.setEdgeWeight(1,2,5)
# graph.setEdgeWeight(2,4,9)
print(graph.isCompleteGraph())
##print(graph.getVertexInDegree(1))
##print(graph.getVertexInDegree(4))
# print(graph.getVertexOutDegree(1))
# print(graph.getVertexOutDegree(4))
# print(graph.isSuccessor(3, 1))
# print(graph.isSuccessor(4, 3))
# print(graph.isPredecessor(1, 3))
# print(graph.getVertexCount())
# print(graph.getEdgeCount())
# print(graph.hasEdge(1, 2))
# print(graph.hasEdge(2, 1))
# print(graph.hasEdge(1, 3))
for i in range(graph.numVertices + 1):
    # Primeira linha (cabeçalho)
    if i == 0:
        print("     ", end="")  # espaço para o canto superior esquerdo
        for j in range(graph.numVertices):
            print(f"{j:>8}", end="")  # cabeçalho das colunas
        print()
    else:
        # Linha da matriz com índice da linha
        print(f"{i - 1:>3} ", end="")  # índice da linha
        for j in range(graph.numVertices):
            peso_vertice, peso_aresta = graph.matrix[i - 1][j]
            print(f"({peso_vertice},{peso_aresta})", end="")
        print()
print()
graph.exportToGEPHI("meu_grafo.gexf")
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