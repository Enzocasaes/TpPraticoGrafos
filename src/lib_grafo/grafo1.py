import os
from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyMatrixGraph import AdjacencyMatrixGraph
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph

mapUser = {}
idRelativo = []


def _init_(self):
    self.map = {}  # GitHub ID → índice 0..N-1
    self.idRelativo = []  # lista inversa: índice → GitHub ID


def getUser(userId):
    # funcao coloca o userId na lista e retorna o id adicionado
    if userId not in mapUser:
        mapUser[userId] = len(mapUser)
        idRelativo.append(userId)
    return mapUser[userId]


def count():
    return len(mapUser)

if __name__ == "__main__":
    client = GithubClient()
    #print(client.getIssuesComments())

    issueComentada = client.getIssuesComments()
    #for para pegar os donos das issues comentadas e adicionar na lista, alem de pegar tambem quem comentou nas issues
    for (idUserComment, idIssue) in issueComentada:
        dono = idUserComment
        getUser(dono)

        comentarios = client.getIssueComments(idIssue)
        #adiciona quem comentou na lista
        for comentario in comentarios:
            quemComentou = comentario["user"]["id"]
            getUser(quemComentou)

    grafo1 = AdjacencyListGraph(count())
    #adicionando arestas
    for (idUserComment, idIssue) in issueComentada:
        dono = idUserComment
        u = getUser(dono)
        print("----->",idIssue)
        print(u)
        comentarios = client.getIssueComments(idIssue)


        for comentario in comentarios:
            quemComentou = comentario["user"]["id"]
            v = getUser(quemComentou)
            print(v)
            grafo1.addEdge(v, u)

        print("-------------------------------------------------------------------------------------")
    grafo1.exportToGEPHI("grafo1List.gexf")