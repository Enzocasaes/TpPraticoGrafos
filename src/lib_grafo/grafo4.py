import os
from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph

mapUser = {}
idRelativo = []

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
    issueComentada = client.getIssuesCommentsParaGrafo1()
    issueAberta = client.getOpenIssues()
    arr_colaborators = client.getColaborators()
    arr_merges = client.getMergedPullRequests()
    arr_reviews = client.getPullRequests()

    for item in issueComentada:
        getUser(item["user"]["id"])

        idIssue = item["issue_url"].split("/")[-1]
        for c in client.getIssueCommentsParaGrafo1(idIssue):
            getUser(c["user"]["id"])

    for idUser in arr_colaborators:
        getUser(idUser)

    for (idUserOpen, idUserCloser) in arr_merges:
        getUser(idUserOpen)
        getUser(idUserCloser)

    for (idReviewer, idOwnerPR) in arr_reviews:
        getUser(idReviewer)
        getUser(idOwnerPR)

    for item in issueComentada:
        idIssue = int(item["issue_url"].split("/")[-1])
        autor = client.getOwnerIdByIssue(idIssue)
        getUser(autor)

    grafo = AdjacencyListGraph(count())

    for item in issueComentada:
        idUserComment = getUser(item["user"]["id"])
        idIssue = item["issue_url"].split("/")[-1]
        autor = getUser(client.getOwnerIdByIssue(idIssue))

        if not grafo.hasEdge(idUserComment, autor):
            grafo.addEdge(idUserComment, autor)
            grafo.setEdgeWeight(idUserComment, autor, 2)
        else:
            grafo.setEdgeWeight(idUserComment, autor, grafo.getEdgeWeight(idUserComment, autor) + 2)

    for item in issueComentada:
        idIssue = int(item["issue_url"].split("/")[-1])
        autor = getUser(client.getOwnerIdByIssue(idIssue))

        for c in client.getIssueCommentsParaGrafo1(idIssue):
            idComentou = getUser(c["user"]["id"])
            if not grafo.hasEdge(autor, idComentou):
                grafo.addEdge(autor, idComentou)
                grafo.setEdgeWeight(autor, idComentou, 3)
            else:
                grafo.setEdgeWeight(autor, idComentou, grafo.getEdgeWeight(autor, idComentou) + 3)

    for (idReviewer, idOwnerPR) in arr_reviews:
        idR = getUser(idReviewer)
        idO = getUser(idOwnerPR)

        if not grafo.hasEdge(idR, idO):
            grafo.addEdge(idR, idO)

        peso_atual = grafo.getEdgeWeight(idR, idO) or 0
        grafo.setEdgeWeight(idR, idO, peso_atual + 4)

    for (idUserOpen, idUserCloser) in arr_merges:
        idAutor = getUser(idUserOpen)
        idMerge = getUser(idUserCloser)

        if not grafo.hasEdge(idMerge, idAutor):
            grafo.addEdge(idMerge, idAutor)
            grafo.setEdgeWeight(idMerge, idAutor, 5)
        else:
            grafo.setEdgeWeight(idMerge, idAutor, grafo.getEdgeWeight(idMerge, idAutor) + 5)

    grafo.exportToGEPHI("grafo4.gexf")
