import math

class Coesao:
    def __init__(self, grafo):
        self.G = grafo

    # -----------------------------------------
    # 1. Densidade
    # -----------------------------------------
    def densidade(self):
        G = self.G
        n = G.getVertexCount()
        m = sum(len(G.adjacencias[u]) for u in range(n))

        max_m = n * (n - 1)
        return m / max_m if max_m > 0 else 0.0

    # -----------------------------------------
    # 2. Clustering
    # -----------------------------------------
    def clustering_global(self):
        G = self.G
        n = G.getVertexCount()
        C = {}

        for v in range(n):
            neighbors = G.adjacencias[v]
            k = len(neighbors)
            if k < 2:
                C[v] = 0.0
                continue

            E = 0
            for u in neighbors:
                for w in neighbors:
                    if w in G.adjacencias[u]:
                        E += 1

            C[v] = E / (k * (k - 1))

        return sum(C.values()) / n

    # -----------------------------------------
    # 3. Assortatividade
    # -----------------------------------------
    def assortatividade(self):
        G = self.G
        n = G.getVertexCount()

        jk = []
        for u in range(n):
            deg_u = len(G.adjacencias[u])
            for v in G.adjacencias[u]:
                deg_v = len(G.adjacencias[v])
                jk.append((deg_u, deg_v))

        if len(jk) < 2:
            return 0.0

        sum_j = sum(j for j, k in jk)
        sum_k = sum(k for j, k in jk)
        sum_jk = sum(j * k for j, k in jk)
        sum_j2 = sum(j * j for j, k in jk)
        sum_k2 = sum(k * k for j, k in jk)

        m = len(jk)

        num = m * sum_jk - sum_j * sum_k
        den = math.sqrt((m * sum_j2 - sum_j * sum_j) * (m * sum_k2 - sum_k * sum_k))

        return num / den if den != 0 else 0.0