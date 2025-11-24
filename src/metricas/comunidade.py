from src.metricas.louvain import louvain

class Comunidade:
    def __init__(self, grafo):
        self.G = grafo

    # -----------------------------------------
    # Modularidade
    # -----------------------------------------
    def modularidade(self, comunidades):
        G = self.G
        n = G.getVertexCount()

        m = sum(len(G.adjacencias[u]) for u in range(n))
        if m == 0:
            return 0.0

        Q = 0.0

        for u in range(n):
            for v in range(n):
                same = 1 if comunidades[u] == comunidades[v] else 0
                A_uv = 1 if v in G.adjacencias[u] else 0

                k_u = len(G.adjacencias[u]) + sum(1 for x in range(n) if u in G.adjacencias[x])
                k_v = len(G.adjacencias[v]) + sum(1 for x in range(n) if v in G.adjacencias[x])

                Q += (A_uv - (k_u * k_v) / m) * same

        return Q / m

    # -----------------------------------------
    # Louvain simplificado
    # -----------------------------------------
    def detectar(self):
        """
        Executa o algoritmo Louvain verdadeiro (implementação em louvain.py)
        e retorna:
            - comunidades: dict {nó → id_da_comunidade}
            - modularidade_final
        """
        comunidades, modularidade = louvain(self.G, resolution=1.0, random_state=42)
        return comunidades, modularidade

    # -----------------------------------------
    # Bridging ties
    # -----------------------------------------
    def bridging(self):
        G = self.G
        n = G.getVertexCount()
        comunidades, _ = self.detectar()

        bridging_edges = []
        scores = {v: 0 for v in range(n)}

        for u in range(n):
            for v in G.adjacencias[u]:
                if comunidades[u] != comunidades[v]:
                    bridging_edges.append((u, v))
                    scores[u] += 1
                    scores[v] += 1

        return bridging_edges, scores