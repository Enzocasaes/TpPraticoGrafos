import sys
import xml.etree.ElementTree as ET
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph
from src.metricas.centralidade import Centralidade
from src.metricas.coesao import Coesao
from src.metricas.comunidade import Comunidade


# =======================
# Função para carregar .GEXF
# =======================
def load_graph_any_format(path):
    tree = ET.parse(path)
    root = tree.getroot()

    # Detecta o namespace real
    ns = root.tag.split("}")[0].strip("{")

    # ===== CASO 1 — GEXF =====
    if "gexf" in ns:
        N_NODE = ".//{http://www.gexf.net/1.2draft}node"
        N_EDGE = ".//{http://www.gexf.net/1.2draft}edge"

        nodes = root.findall(N_NODE)
        edges = root.findall(N_EDGE)

        id_map = {n.get("id"): i for i, n in enumerate(nodes)}
        G = AdjacencyListGraph(len(nodes))

        for e in edges:
            u = id_map[e.get("source")]
            v = id_map[e.get("target")]
            w = float(e.get("weight", 1.0))
            G.addEdge(u, v)
            G.setEdgeWeight(u, v, w)

        return G

    # ===== CASO 2 — GRAPHML =====
    elif "graphml" in ns:
        # GRAPHML usa seu namespace próprio
        N_NODE = ".//{%s}node" % ns
        N_EDGE = ".//{%s}edge" % ns

        nodes = root.findall(N_NODE)
        edges = root.findall(N_EDGE)

        id_map = {n.get("id"): i for i, n in enumerate(nodes)}
        G = AdjacencyListGraph(len(nodes))

        for e in edges:
            u = id_map[e.get("source")]
            v = id_map[e.get("target")]
            G.addEdge(u, v)

        return G

    else:
        raise ValueError(f"Formato desconhecido: namespace {ns}")




# =======================
# MAIN MÉTRICAS
# =======================
def main():
    if len(sys.argv) < 2:
        print("Uso: python main_metricas.py arquivo.gexf")
        return

    path = sys.argv[1]
    G = load_graph_any_format(path)

    print("\n===== ANÁLISE DO GRAFO =====\n")

    # CENTRALIDADE
    central = Centralidade(G)
    print("Degree:", central.degree())
    print("Betweenness:", central.betweenness())
    print("Closeness:", central.closeness())
    print("PageRank:", central.pagerank())
    print("Eigenvector:", central.eigenvector())

    # ESTRUTURA / COESÃO
    coesao = Coesao(G)
    print("\nDensidade:", coesao.densidade())
    print("Clustering:", coesao.clustering_global())
    print("Assortatividade:", coesao.assortatividade())

    # COMUNIDADES
    comunidade = Comunidade(G)
    comunidades, modularidade = comunidade.detectar()
    print("\nModularidade:", modularidade)
    print("Comunidades:", comunidades)

    bridging_edges, bridging_score = comunidade.bridging()
    print("Bridging ties:", bridging_edges)
    print("Bridging score:", bridging_score)


if __name__ == "__main__":
    main()
