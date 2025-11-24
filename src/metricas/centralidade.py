import math

class Centralidade:
    def __init__(self, grafo):
        self.G = grafo

    # -----------------------------------------
    # Grau (degree centrality)
    # -----------------------------------------
    def degree(self):
        G = self.G
        n = G.getVertexCount()
        C = {}

        for v in range(n):
            grau = G.getVertexOutDegree(v) + G.getVertexInDegree(v)
            C[v] = grau / (n - 1)

        return C

    # -----------------------------------------
    # Betweenness (Brandes)
    # -----------------------------------------
    def betweenness(self):
        G = self.G
        n = G.getVertexCount()
        Cb = {v: 0.0 for v in range(n)}

        for s in range(n):
            S = []
            P = {w: [] for w in range(n)}
            sigma = {w: 0.0 for w in range(n)}
            dist = {w: math.inf for w in range(n)}

            sigma[s] = 1.0
            dist[s] = 0
            Q = [s]

            # BFS
            while Q:
                v = Q.pop(0)
                S.append(v)

                for w in G.adjacencias[v]:
                    if dist[w] == math.inf:
                        dist[w] = dist[v] + 1
                        Q.append(w)

                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        P[w].append(v)

            delta = {v: 0.0 for v in range(n)}

            while S:
                w = S.pop()
                for v in P[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    Cb[w] += delta[w]

        fator = 1 / ((n - 1) * (n - 2))
        for v in Cb:
            Cb[v] *= fator

        return Cb

    # -----------------------------------------
    # Closeness
    # -----------------------------------------
    def closeness(self):
        G = self.G
        n = G.getVertexCount()
        Cc = {}

        for s in range(n):
            dist = {v: math.inf for v in range(n)}
            dist[s] = 0
            Q = [s]

            while Q:
                v = Q.pop(0)
                for w in G.adjacencias[v]:
                    if dist[w] == math.inf:
                        dist[w] = dist[v] + 1
                        Q.append(w)

            total = sum(dist.values())
            Cc[s] = (n - 1) / total if total > 0 else 0.0

        return Cc

    # -----------------------------------------
    # PageRank
    # -----------------------------------------
    def pagerank(self, d=0.85, max_iter=100, tol=1e-6):
        G = self.G
        n = G.getVertexCount()
        PR = {v: 1.0 / n for v in range(n)}

        for _ in range(max_iter):
            newPR = {}
            for v in range(n):
                soma = 0
                for u in range(n):
                    if v in G.adjacencias[u]:
                        deg = len(G.adjacencias[u])
                        if deg > 0:
                            soma += PR[u] / deg

                newPR[v] = (1 - d) / n + d * soma

            if sum(abs(newPR[v] - PR[v]) for v in range(n)) < tol:
                break

            PR = newPR

        return PR

    # -----------------------------------------
    # Eigenvector
    # -----------------------------------------
    def eigenvector(self, max_iter=100, tol=1e-6):
        G = self.G
        n = G.getVertexCount()

        # vetor inicial
        x = {v: 1.0 for v in range(n)}

        for _ in range(max_iter):
            new_x = {}
            norm = 0.0

            # Multiplicação A * x
            for v in range(n):
                soma = 0.0
                for u in range(n):
                    if v in G.adjacencias[u]:
                        soma += x[u]
                new_x[v] = soma
                norm += soma * soma

            norm = math.sqrt(norm)

            # Caso especial: grafo desconexo ou sem estrutura suficiente
            if norm == 0:
                # Não é possível normalizar — retorna vetor de zeros
                return {v: 0.0 for v in range(n)}

            # normaliza
            for v in new_x:
                new_x[v] /= norm

            # critério de convergência
            if sum(abs(new_x[v] - x[v]) for v in range(n)) < tol:
                return new_x

            x = new_x

        return x