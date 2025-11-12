
from __future__ import annotations
import os
from typing import Dict, List, Tuple

from src.mineracao.client_github import GithubClient
from src.lib_grafo.AdjacencyListGraph import AdjacencyListGraph


def build_graph_from_client(client: GithubClient, out_nodes: str = "nodes.csv", out_edges: str = "edges.csv") -> AdjacencyListGraph:
    comments = []
    try:
        comments = client.getIssuesComments() or []
    except Exception:
        try:
            issues = client.getIssues() or []
            for iss in issues:
                iid = iss.get("number")
                if iid:
                    cs = client.getIssueComments(str(iid)) or []
                    comments.extend(cs)
        except Exception:
            pass

    issues_map: Dict[str, str] = {}
    try:
        open_issues = client.getOpenIssues() or []
    except Exception:
        open_issues = []
    try:
        closed_issues = client.getClosedIssues() or []
    except Exception:
        closed_issues = []

    for iss in open_issues + closed_issues:
        url = iss.get("url")
        user = None
        u = iss.get("user")
        if u:
            user = u.get("login")
        if url and user:
            issues_map[url] = user

    comment_id_to_user: Dict[int, str] = {}
    for c in comments:
        cid = c.get("id")
        u = c.get("user")
        if cid and u:
            login = u.get("login")
            if login:
                try:
                    comment_id_to_user[int(cid)] = login
                except Exception:
                    pass

    logins = set()
    for user in issues_map.values():
        if user:
            logins.add(user)
    for c in comments:
        u = c.get("user")
        if u:
            login = u.get("login")
            if login:
                logins.add(login)
    sorted_logins = sorted(logins)
    login_to_idx: Dict[str, int] = {login: i for i, login in enumerate(sorted_logins)}

    g = AdjacencyListGraph(len(sorted_logins))

    for c in comments:
        user_obj = c.get("user")
        if not user_obj:
            continue
        src_login = user_obj.get("login")
        if not src_login:
            continue

        target_login = None
        in_reply = c.get("in_reply_to_id")
        if in_reply:
            try:
                target_login = comment_id_to_user.get(int(in_reply))
            except Exception:
                target_login = None

        if not target_login:
            issue_url = c.get("issue_url")
            if issue_url:
                target_login = issues_map.get(issue_url)

        if not target_login:
            continue

        if src_login == target_login:
            continue

        src_idx = login_to_idx.get(src_login)
        tgt_idx = login_to_idx.get(target_login)
        if src_idx is None or tgt_idx is None:
            continue

        g.addEdge(src_idx, tgt_idx)

    with open(out_nodes, "w", encoding="utf-8") as f:
        f.write("id,login\n")
        for login, idx in sorted(login_to_idx.items(), key=lambda x: x[1]):
            f.write(f"{idx},{login}\n")

    with open(out_edges, "w", encoding="utf-8") as f:
        f.write("source,target\n")
        for u, neigh in g.adjacencias.items():
            for v in neigh:
                f.write(f"{u},{v}\n")

    return g


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerar grafo a partir do client_github existente")
    parser.add_argument("--nodes", default="nodes.csv", help="arquivo nodes CSV")
    parser.add_argument("--edges", default="edges.csv", help="arquivo edges CSV")
    args = parser.parse_args()

    client = GithubClient()
    print("Buscando dados via client_github...")
    g = build_graph_from_client(client, out_nodes=args.nodes, out_edges=args.edges)
    print(f"Gerado grafo: vértices={g.getVertexCount()}, arestas={g.getEdgeCount()}")
