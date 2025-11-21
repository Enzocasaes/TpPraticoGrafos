import os
import requests
import re

class GithubClient:
    URLBASE = "https://api.github.com/repos/sorrycc/awesome-javascript"

    def __init__(self):
        auth_token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization" : f"Bearer {auth_token}"
        }


    def getIssues(self):
        ulrBusca = f"{GithubClient.URLBASE}/issues"
        issues = requests.get(url=ulrBusca, headers=self.headers).json()

        arr_id_issues = []
        for issue in issues:
            arr_id_issues.append(issue["number"])

        return arr_id_issues

    def getOwnerIdByIssue(self, issueId):
        ulrBusca = "https://api.github.com/graphql"

        variables = {
            "owner": "sorrycc",
            "repoName": "awesome-javascript",
            "issueNumber": issueId
        }

        query = """
            query GetAssigneeId($owner: String!, $repoName: String!, $issueNumber: Int!) {
                repository(owner: $owner, name: $repoName) { 
                  issue(number: $issueNumber) { 
                    assignees(first: 1) { 
                      nodes { 
                        databaseId 
                      } 
                    } 
                  } 
                } 
            }     
        """

        payload = {
            "query": query,
            "variables": variables
        }

        response = requests.post(url=ulrBusca, headers=self.headers, json=payload).json()
        if response.get("errors"):
            print(f"Erro GQL na issue {issueId}: {response['errors'][0]['message']}")
            return None

        issue = response["data"]["repository"].get("issue")
        if issue is None:
            print(f"Issue {issueId} não encontrada ou não existe.")
            return None

        assignee_nodes = issue.get("assignees", {}).get("nodes", [])
        if assignee_nodes:
            owner_id = assignee_nodes[0].get("databaseId")
            return owner_id
        else:
            print(f"Issue {issueId} não possui responsável (assignee).")
            return None

    def getIssuesComments(self):
        base_url = f"{GithubClient.URLBASE}/issues/comments"
        page = 1
        arr_users_comments = []

        while True:
            url_busca_paginada = f"{base_url}?page={page}&per_page=100"

            print(f"Buscando página {page} de comentários...")
            response = requests.get(url=url_busca_paginada, headers=self.headers)

            if response.status_code != 200:
                print(f"Erro ao buscar comentários: Status {response.status_code}")
                break

            arr_issues_comments = response.json()

            if not arr_issues_comments:
                break

            for comment in arr_issues_comments:
                issue_url = comment["issue_url"]
                id_user = comment["user"]["id"]

                match = re.search(r"\/(\d+)$", issue_url)
                if match:
                    id_issue = int(match.group(1))

                issue_author_id = self.getOwnerIdByIssue(id_issue)

                if id_user != issue_author_id:
                    print("Tupla inserida")
                    arr_users_comments.append((id_user, id_issue))

            page += 1
        return arr_users_comments

    def getIssueComments(self, issueId: str):
        urlBusca = f"{GithubClient.URLBASE}/issues/{issueId}/comments"
        return requests.get(url=urlBusca, headers=self.headers).json()

    def getClosedIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues"
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json()

    def getOpenIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues"
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json()

    def getOpenPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls"
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json()

    def getClosedPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls"
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json()

    def getMergedPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls"
        arr_pulls = requests.get(url=urlBusca, headers=self.headers, params={"state": "all"}).json()
        arr_pulls_merged = []

        for pull in arr_pulls:
            if pull["merged_at"]:
                arr_pulls_merged.append(pull)

        return arr_pulls_merged

    def getUsersFromOpenIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues"
        arr_issues = requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json()

        arr_users = []
        for issue in arr_issues:
            assignee = issue.get("user")

            if assignee:
                login = assignee.get("login")
                if login:
                    arr_users.append(login)

        return arr_users

    def getUsersFromClosedIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues"
        arr_issues = requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json()

        arr_users = []
        for issue in arr_issues:
            assignee = issue.get("user")

            if assignee:
                userId = assignee.get("id")
                if userId:
                    arr_users.append(userId)

        return arr_users