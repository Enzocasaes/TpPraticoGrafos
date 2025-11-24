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

    def getAllPaginated(self, url):
        results = []
        headers = self.headers

        while url:
            r = requests.get(url=url, headers=headers)
            r.raise_for_status()

            results.extend(r.json())

            # pega link de paginação
            link = r.headers.get("Link", "")
            url_next = None

            if 'rel="next"' in link:
                parts = link.split(",")
                for part in parts:
                    if 'rel="next"' in part:
                        url_next = part[part.find("<") + 1: part.find(">")]
                        break

            url = url_next

        return results


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
            "issueNumber": int(issueId)
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

    def getIssuesCommentsParaGrafo1(self):
        urlBusca = f"{GithubClient.URLBASE}/issues/comments"
        return self.getAllPaginated(urlBusca)

    def getPullRequestReviews(self):
        reviews = []
        urlBase = f"{GithubClient.URLBASE}/pulls"
        page = 1

        while True:
            urlBusca = f"{urlBase}?state=all&page={page}&per_page=20"
            response = requests.get(url=urlBusca, headers=self.headers)

            if response.status_code != 200:
                break

            pulls = response.json()
            if not pulls:
                break

            for pr in pulls:
                pr_number = pr["number"]
                owner = pr["user"]["id"]

                urlReviews = f"{urlBase}/{pr_number}/reviews"
                rev_response = requests.get(urlReviews, headers=self.headers)

                if rev_response.status_code != 200:
                    continue

                arr_reviews = rev_response.json()
                for rev in arr_reviews:
                    reviewer = rev["user"]["id"]
                    reviews.append((reviewer, owner))

            page += 1
        return reviews

    def getIssueCommentsParaGrafo1(self, issueId: str):
        urlBusca = f"{GithubClient.URLBASE}/issues/{issueId}/comments"
        return requests.get(url=urlBusca, headers=self.headers).json()
        ##return self.getAllPaginated(urlBusca)

    def getIssuesComments(self):
        base_url = f"{GithubClient.URLBASE}/issues/comments"
        page = 1
        arr_users_comments = []

        while True:
            url_busca_paginada = f"{base_url}?page={page}&per_page=20"

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
        urlBusca = f"{GithubClient.URLBASE}/issues?state=closed&per_page=100"
        return self.getAllPaginated(urlBusca)

    def getOpenIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues"
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json()

    def getPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls"
        print(urlBusca)
        page = 1
        arr_pulls = []
        while True:
            params = {
                "state": "all",
                "page": page,
                "per_page": 100
            }
            response = requests.get(url=urlBusca, headers=self.headers,params=params)
            print(response.url)
            if response.status_code != 200:
                print(f"Erro ao realizar requisição para prs: {response.status_code}")
                break

            arr_prs = response.json()

            if not arr_prs:
                break

            for pr in arr_prs:
                if not pr.get("user"):
                    continue

                id_author = pr.get("user")["id"]
                urlBusca = f"{GithubClient.URLBASE}/pulls/{pr['number']}/reviews"
                print(urlBusca)
                reviewResponse = requests.get(url=urlBusca, headers=self.headers)

                if reviewResponse.status_code != 200:
                    print(f"Erro ao realizar consulta pr: {pr['number']}")
                    break

                detailedReview = reviewResponse.json()
                if not detailedReview:
                    continue
                else:
                    detailedReview = detailedReview[0]
                    id_reviewer = detailedReview.get("user")["id"]


                if id_author == id_reviewer:
                    continue

                state = detailedReview["state"]
                if state in ["APPROVED","CHANGES_REQUESTED", "COMMENTED"]:
                    arr_pulls.append((id_author, id_reviewer))

        return arr_pulls

    def getMergedPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls"
        page = 1
        arr_merge = []

        while True:
            params = {
                "state":"closed",
                "page": page,
                "per_page": 100
            }
            response = requests.get(url=urlBusca, headers=self.headers,params=params)

            if response.status_code != 200:
                print(f"Erro ao realizar requisição para pull requests (merges): {response.status_code}")
                break

            arr_merges_response = response.json()

            if not arr_merges_response:
                break

            for merge in arr_merges_response:
                if merge["merged_at"] is None:
                    continue

                id_user_open_merge = merge["user"]["id"]
                issue_url = merge["issue_url"]

                issue_response = requests.get(url=issue_url, headers=self.headers)
                if issue_response.status_code != 200:
                    print(f"Erro ao realizar requisição issue {issue_url}: {issue_response.status_code}")
                    continue


                issue = issue_response.json()
                if issue.get("closed_by") is None:
                    continue

                id_user_close_merge = issue.get("closed_by")["id"]

                if id_user_close_merge == id_user_open_merge:
                    continue

                if len(arr_merge) >= 50:
                    return arr_merge

                arr_merge.append((id_user_open_merge, id_user_close_merge))
                print(f"Tupla inserida: {id_user_open_merge},{id_user_close_merge}")

            page += 1
        return arr_merge

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

    def getColaborators(self):
        url = f"{GithubClient.URLBASE}/contributors"
        page = 1
        arr_contributors = []

        while(True):
            urlBusca = f"{url}?page={page}&per_page=20"
            response = requests.get(url=urlBusca, headers=self.headers)

            if response.status_code != 200:
                print(f"Erro ao buscar comentários: Status {response.status_code}")
                break

            arr_response = response.json()

            if not arr_response:
                break

            for colaborator in arr_response:
                userId = colaborator['id']
                if userId:
                    arr_contributors.append(userId)

            page += 1
        return arr_contributors