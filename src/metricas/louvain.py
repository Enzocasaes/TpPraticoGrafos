# src/metricas/louvain.py
import math
from collections import defaultdict
import copy
import random

def _safe_weight(weight):
    """Converte peso possivelmente nulo/str para float; default 1.0"""
    try:
        if weight is None:
            return 1.0
        return float(weight)
    except Exception:
        return 1.0

def to_undirected_weighted_adj(G):
    """
    Constrói um dicionário de adjacência não-direcionado com pesos a partir do
    AdjacencyListGraph direcionado do seu projeto.
    Retorna: adj (dict node -> dict(neighbor -> weight)), nodes list
    """
    n = G.getVertexCount()
    adj = {i: defaultdict(float) for i in range(n)}

    for u in range(n):
        for v in G.adjacencias[u]:
            w = G.getEdgeWeight(u, v)
            w = _safe_weight(w)
            adj[u][v] += w
            adj[v][u] += w  # tornar não direcionado somando nos dois sentidos

    # remove possíveis zeros e converte para dict normal
    for u in adj:
        adj[u] = {v: w for v, w in adj[u].items() if w != 0}

    return adj, list(range(n))

def total_edge_weight(adj):
    """Retorna m = soma total dos pesos das arestas (cada aresta contada uma vez)"""
    total = 0.0
    for u, nbrs in adj.items():
        total += sum(nbrs.values())
    return total / 2.0

def initial_partition(nodes):
    """Inicialmente cada nó em sua própria comunidade"""
    return {node: node for node in nodes}

def _compute_degrees(adj):
    """Grau (soma de pesos) de cada nó"""
    return {u: sum(adj[u].values()) for u in adj}

def _community_totals_and_internals(partition, adj, degrees):
    """
    Calcula:
     - tot[c] = soma dos graus (k_i) dos nós na comunidade c
     - in_weight[c] = soma dos pesos das arestas internas na comunidade c (cada aresta contada uma vez)
    """
    tot = defaultdict(float)
    in_w = defaultdict(float)

    for u, com in partition.items():
        tot[com] += degrees.get(u, 0.0)

    # para in_w: para cada aresta u-v (u<=v) se partition[u]==partition[v] soma o peso
    seen = set()
    for u, nbrs in adj.items():
        for v, w in nbrs.items():
            if (v, u) in seen:
                continue
            seen.add((u, v))
            if partition[u] == partition[v]:
                in_w[partition[u]] += w

    return tot, in_w

def _neighcom(node, adj, partition):
    """
    Retorna dict: community -> total weight of edges from node to that community
    """
    weights = defaultdict(float)
    for nei, w in adj[node].items():
        weights[partition[nei]] += w
    return weights

def _remove_node(node, com, tot, in_w, degrees, neigh_weights):
    """
    Remove efeito de node da sua comunidade 'com' atual:
    atualiza tot[com] e in_w[com]
    neigh_weights: peso de node para sua comunidade (k_i_in) já calculado
    """
    tot[com] -= degrees[node]
    # ao remover, as arestas entre node e outros nós da comunidade deixam de ser internas:
    # cada aresta para comunidade contribui com w em k_i_in, e interna total perde 2*k_i_in
    in_w[com] -= 2.0 * neigh_weights.get(com, 0.0)

def _insert_node(node, com, tot, in_w, degrees, neigh_weights):
    """
    Insere node na comunidade com: atualiza tot e in_w
    """
    # quando inserir, arestas entre node e comunidade viram internas -> incrementam 2*k_i_in
    in_w[com] += 2.0 * neigh_weights.get(com, 0.0)
    tot[com] += degrees[node]

def _modularity_from_state(partition, adj, degrees, m):
    """
    Calcula modularidade Q dado estado atual.
    Fórmula (para grafos não direcionados, ponderados):
    Q = (1/(2m)) * sum_c ( in_c - (tot_c^2) / (2m) )
    onde in_c é a soma dos pesos das arestas internas em c,
    tot_c é a soma dos graus dos nós em c.
    """
    tot = defaultdict(float)
    in_w = defaultdict(float)

    for u in adj:
        tot[partition[u]] += degrees[u]
    seen = set()
    for u, nbrs in adj.items():
        for v, w in nbrs.items():
            if (v, u) in seen:
                continue
            seen.add((u, v))
            if partition[u] == partition[v]:
                in_w[partition[u]] += w

    Q = 0.0
    if m <= 0:
        return 0.0
    for c in tot:
        Q += in_w[c] - (tot[c] * tot[c]) / (2.0 * m)
    return Q / (2.0 * m)

def one_level(adj, nodes, partition, m, resolution=1.0):
    """
    Executa uma única fase "local" do Louvain: tenta mover cada nó para a comunidade
    vizinha que maximiza ganho de modularidade.
    Retorna (partition, improved) e as estruturas tot/in atualizadas.
    """
    degrees = _compute_degrees(adj)
    tot, in_w = _community_totals_and_internals(partition, adj, degrees)

    improved = False
    mod_before = _modularity_from_state(partition, adj, degrees, m)

    nodes_list = list(nodes)
    random.shuffle(nodes_list)

    for node in nodes_list:
        com_node = partition[node]
        neigh_weights = _neighcom(node, adj, partition)
        k_i = degrees[node]
        # remove node temporariamente
        _remove_node(node, com_node, tot, in_w, degrees, neigh_weights)
        partition[node] = -1  # marca como sem comunidade

        best_com = com_node
        best_increase = 0.0  # considerar 0 como baseline (não mover)

        # considerar comunidades vizinhas
        for com, k_i_in in neigh_weights.items():
            # fórmula do ganho de modularidade (Blondel et al.)
            # deltaQ = [k_i_in - (k_i * tot[com]) / (2m)] / (2m)
            delta = (k_i_in - (k_i * tot[com]) / (2.0 * m)) / (2.0 * m)
            # aplicar resolução (gamma) se desejar (multiplica k_i_in por resolution)
            # se usar resolution, a fórmula se ajusta para: delta = (resolution * k_i_in - (k_i * tot[com]) / (2m)) / (2m)
            # para manter compatibilidade, multiplico só k_i_in:
            if resolution != 1.0:
                delta = (resolution * k_i_in - (k_i * tot[com]) / (2.0 * m)) / (2.0 * m)

            if delta > best_increase:
                best_increase = delta
                best_com = com

        # se melhor comunidade encontrada, insere lá; senão re-insere na original
        partition[node] = best_com
        if best_com != com_node:
            improved = True

        # atualizar estruturas com a inserção
        # (neigh_weights[best_com] pode ser 0 se moveu para comunidade sem aresta direta)
        _insert_node(node, partition[node], tot, in_w, degrees, neigh_weights)

    mod_after = _modularity_from_state(partition, adj, degrees, m)
    return partition, improved, mod_before, mod_after, tot, in_w

def induced_graph(partition, adj):
    """
    Constrói o grafo induzido onde cada comunidade vira um nó.
    Retorna (new_adj, new_nodes, node_to_com mapping inversa: com -> [nodes])
    """
    com_nodes = defaultdict(list)
    for node, com in partition.items():
        com_nodes[com].append(node)

    com_index = {com: idx for idx, com in enumerate(com_nodes.keys())}
    new_adj = {com_index[c]: defaultdict(float) for c in com_nodes}

    # para cada aresta u-v no grafo original, soma peso entre communities
    for u, nbrs in adj.items():
        cu = com_index[partition[u]]
        for v, w in nbrs.items():
            cv = com_index[partition[v]]
            new_adj[cu][cv] += w

    # converte inner dicts para dict e lista nodes
    for k in list(new_adj.keys()):
        new_adj[k] = dict(new_adj[k])

    new_nodes = list(new_adj.keys())
    return new_adj, new_nodes, com_nodes

def renumber_partition(partition):
    """
    Renumera comunidades para ids 0..k-1 e retorna novo partition dict.
    """
    coms = {}
    new_id = 0
    new_partition = {}
    for node, com in partition.items():
        if com not in coms:
            coms[com] = new_id
            new_id += 1
        new_partition[node] = coms[com]
    return new_partition

def louvain(G, resolution=1.0, random_state=None, verbose=False):
    """
    Implementação completa do método Louvain.
    Entrada:
        G: AdjacencyListGraph do seu projeto
        resolution: parâmetro de resolução gamma
    Retorna:
        final_partition (dict node -> community), final_modularity
    """
    if random_state is not None:
        random.seed(random_state)

    adj, nodes = to_undirected_weighted_adj(G)
    if len(nodes) == 0:
        return {}, 0.0

    degrees = _compute_degrees(adj)
    m = total_edge_weight(adj)
    if m <= 0:
        # grafo sem arestas
        return {n: i for i, n in enumerate(nodes)}, 0.0

    # inicial partition
    current_partition = initial_partition(nodes)
    current_adj = adj
    current_nodes = nodes

    hierarchy = []  # guardamos partições para reconstruir ao final se quisermos

    improvement = True
    prev_mod = _modularity_from_state(current_partition, current_adj, degrees, m)
    if verbose:
        print("Louvain: m =", m, "n =", len(nodes), "mod_init =", prev_mod)

    while improvement:
        # fase local repetida até não melhorar
        moved = True
        while moved:
            current_partition, moved, mod_before, mod_after, tot, in_w = one_level(current_adj, current_nodes, current_partition, m, resolution)
            if verbose:
                print(f"  one_level: mod_before={mod_before:.6f} mod_after={mod_after:.6f} moved={moved}")
        # após fase local sem movimentos, computa nova partição e gera grafo induzido
        new_mod = _modularity_from_state(current_partition, current_adj, _compute_degrees(current_adj), m)
        if verbose:
            print("  modularity after local phase:", new_mod)

        # condicional de parada: se não houver ganho relevante
        if new_mod - prev_mod < 1e-7:
            improvement = False
            break

        prev_mod = new_mod

        # comprimir grafo
        new_adj, new_nodes, com_nodes = induced_graph(current_partition, current_adj)

        # reconstroi dados para próxima iteração
        current_adj = new_adj
        current_nodes = new_nodes
        # reset partition: cada comunidade vira seu próprio nó (id: node index)
        current_partition = {n: n for n in current_nodes}
        degrees = _compute_degrees(current_adj)
        m = total_edge_weight(adj)  # m sempre referente ao grafo original: keep as original total weight
        # note: using original m allows modularity formula consistent across levels
        hierarchy.append(com_nodes)

    # Ao final, reconstruir partição final dos nós originais:
    # A cada nível de hierarchy, expandimos as comunidades.
    # Se não houve compressão (hierarchy empty), current_partition já é final.
    if not hierarchy:
        final_partition = renumber_partition(current_partition)
        final_mod = _modularity_from_state(final_partition, adj, _compute_degrees(adj), total_edge_weight(adj))
        return final_partition, final_mod

    # Se houve compressões, reconstruir mapeamento:
    # hierarchy[0] = mapping comunidade_lvl0 -> list(orig_nodes)
    # hierarchy[1] = mapping comunidade_lvl1 -> list(nodes_lvl0), etc.
    # Vamos reconstruir de trás pra frente.
    # Começamos com a última partition (current_partition) que mapeia nodes_lvlK -> community_lvlK
    last_partition = current_partition  # nodes at top-level -> same id
    # map_top maps top_level_node -> set(orig_nodes)
    map_top = {}
    # start with the last hierarchy level (a dict com_id -> list(nodes previous level))
    # reconstruct iteratively:
    map_level = {n: set([n]) for n in last_partition.keys()}  # each top node initially represents itself (ids are ints)
    # iterate hierarchy in reverse
    for level in reversed(hierarchy):
        # level: dict community_id_at_previous_step -> list(nodes in previous step)
        new_map_level = {}
        # for each community_id in level, expand using map_level
        for com_id, members in level.items():
            combined = set()
            for member in members:
                # 'member' is an id from previous step; it may be a key in map_level
                if member in map_level:
                    combined.update(map_level[member])
                else:
                    # fallback: treat member as atomic
                    combined.add(member)
            new_map_level[com_id] = combined
        map_level = new_map_level

    # agora map_level dá comunidades de nível 0 (originais) agrupadas por comunidade final id
    # criar final partition
    final_part = {}
    for com_id, members in map_level.items():
        for node in members:
            final_part[node] = com_id

    final_part = renumber_partition(final_part)
    final_mod = _modularity_from_state(final_part, adj, _compute_degrees(adj), total_edge_weight(adj))

    return final_part, final_mod