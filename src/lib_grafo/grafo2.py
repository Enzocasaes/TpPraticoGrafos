import os
from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph

mapUser = {}
idRelativo = []
def __init__(self):
    self.map = {}
    self.idRelativo = []

def getUser(userId):
    #funcao coloca o userId na lista e retorna o id adicionado
    if userId not in mapUser:
        mapUser[userId] = len(mapUser)
        idRelativo.append(userId)
    return mapUser[userId]

def count():
    return len(mapUser)


if __name__ == "__main__":
    client = GithubClient()
    #print(client.getClosedIssues())

    issueFechada = client.getClosedIssues()

    #esse for pega todos os vertices do grafo(tanto usuarios que abriram quanto os que fecharam), e colocando no map(lista)
    for issue in issueFechada:
        quemAbriu = issue["user"]["id"]
        quemFechou = issue["closed_by"]["id"]

        getUser(quemAbriu)
        getUser(quemFechou)


    grafo2 = AdjacencyListGraph(count())
    #esse for passa por todas as issues fechadas e pegas os usuarios e gera as arestas
    for issue in issueFechada:
        quemAbriu = issue["user"]["id"]
        quemFechou = issue["closed_by"]["id"]
        u = getUser(quemAbriu)
        v = getUser(quemFechou)

        grafo2.addEdge(v, u)

    grafo2.exportToGEPHI("grafo2.gexf")






