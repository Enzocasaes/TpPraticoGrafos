import os
from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph

mapUser = {}
idRelativo = []


def getUser(userId):
    """
    Registra um usuário novo e retorna seu ID convertido
    """
    if userId not in mapUser:
        mapUser[userId] = len(mapUser)
        idRelativo.append(userId)
    return mapUser[userId]


def count():
    return len(mapUser)


if __name__ == "__main__":
    client = GithubClient()

    # Todas as issues fechadas (paginação corrigida)
    issueFechada = client.getClosedIssues()

    # ===== REGISTRA TODOS OS USUÁRIOS (ABRIRAM / FECHARAM) =====
    for issue in issueFechada:
        # Quem abriu a issue
        quemAbriu = issue["user"]["id"]
        getUser(quemAbriu)

        # Quem fechou a issue (pode ser None!)
        closed_by = issue["closed_by"]
        if closed_by is None:
            # Issue fechada automaticamente ou via PR
            # Não incluímos usuário inexistente
            continue

        quemFechou = closed_by["id"]
        getUser(quemFechou)

    # ===== CRIA O GRAFO =====
    grafo2 = AdjacencyListGraph(count())

    # ===== ADICIONA ARESTAS (quem FECHOU → quem ABRIU) =====
    for issue in issueFechada:
        quemAbriu = issue["user"]["id"]
        closed_by = issue["closed_by"]

        # pula issues sem quem fechou
        if closed_by is None:
            continue

        quemFechou = closed_by["id"]

        u = getUser(quemAbriu)
        v = getUser(quemFechou)

        # Aresta: fechador -> abridor
        grafo2.addEdge(v, u)

    # ===== EXPORTA PARA GEPHI =====
    grafo2.exportToGEPHI("grafo2.gexf")

    print("grafo2.gexf gerado com sucesso!")
