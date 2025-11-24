# construção grafo 3 pull requests e merge de pull request
from itertools import count

from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph
from src.lib_grafo.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.mineracao.client_github import GithubClient

mapUser = {}
idRelativo = []

def getUser(userId):
    if userId not in mapUser:
        mapUser[userId] = len(mapUser)
        idRelativo.append(userId)
    return mapUser[userId]

def count():
    return len(mapUser)


if __name__ == "__main__":
    client = GithubClient()

    arr_pulls = client.getPullRequests()
    arr_colaborators = client.getColaborators()
    arr_merges = client.getMergedPullRequests()

    for idUser in arr_colaborators:
        getUser(idUser)
        print(f"Usuario adicionado: {idUser}")

    for (idUserOpen, idUserReviwer) in arr_pulls:
        getUser(idUserOpen)
        getUser(idUserReviwer)

    for (idUserOpen, idUserCloser) in arr_merges:
        getUser(idUserOpen)
        getUser(idUserCloser)



    grafo = AdjacencyMatrixGraph(count())

    for idUser in idRelativo:
        v = getUser(idUser)
        grafo.setVertexWeight(v, idUser)

    for (idUserOpen, idUserCloser) in arr_merges:
        v = getUser(idUserCloser)
        u = getUser(idUserOpen)

        grafo.addEdge(v, u)
        grafo.setEdgeWeight(v, u, 5)

    for (idUserOpen, idUserCloser) in arr_pulls:
        v = getUser(idUserCloser)
        u = getUser(idUserOpen)

        grafo.addEdge(v, u)
        grafo.setEdgeWeight(v, u, 4)

    grafo.exportToGEPHI("grafo3.gexf")