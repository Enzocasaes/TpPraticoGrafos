import os
from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph

mapUser = {}
idRelativo = []

def __init__(self):
    self.map = {}  # GitHub ID → índice 0..N-1
    self.idRelativo = []  # lista inversa: índice → GitHub ID

def getUser(userId):
    if userId not in mapUser:
        mapUser[userId] = len(mapUser)
        idRelativo.append(userId)
    return mapUser[userId]

def count():
    return len(mapUser)


if __name__ == "__main__":
    client = GithubClient()

    issueComentada = client.getIssuesCommentsParaGrafo1()
    #for para pegar os donos das issues comentadas e adicionar na lista, alem de pegar tambem quem comentou nas issues
    for item in issueComentada:
        idUserComment = item["user"]["id"]

        # extrair id da issue a partir da URL
        issue_url = item["issue_url"]
        idIssue = issue_url.split("/")[-1]

        getUser(idUserComment)

        comentarios = client.getIssueCommentsParaGrafo1(idIssue)


        for comentario in comentarios:
            quemComentou = comentario["user"]["id"]
            getUser(quemComentou)

    grafo1 = AdjacencyListGraph(count())

    for item in issueComentada:
        idUserComment = item["user"]["id"]

        issue_url = item["issue_url"]
        idIssue = issue_url.split("/")[-1]

        u = getUser(idUserComment)
        comentarios = client.getIssueCommentsParaGrafo1(idIssue)

        for comentario in comentarios:
            quemComentou = comentario["user"]["id"]
            v = getUser(quemComentou)


            grafo1.addEdge(v, u)

        print("-------------------------------------------------------------------------------------")

    grafo1.exportToGEPHI("grafo1.gexf")
