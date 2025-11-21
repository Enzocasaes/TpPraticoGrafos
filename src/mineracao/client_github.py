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
        ulrBusca = f"{GithubClient.URLBASE}/issues/{issueId}"
        issue = requests.get(url=ulrBusca, headers=self.headers).json()
        user = issue.get("user")
        if user:
            return user.get("id")

    def getIssuesComments(self):
        ulrBusca = f"{GithubClient.URLBASE}/issues/comments"
        arr_issues_comments = requests.get(url=ulrBusca, headers=self.headers).json()
        arr_users_comments = []

        for issue in arr_issues_comments:
            if issue["author_association"] == "OWNER":
                continue

            issue_url = issue["issue_url"]
            if issue_url:
                match = re.search(r"\/(\d+)$", issue_url)
                if match:
                    id_issue = match.group(1)

            user = issue.get("user")
            if user:
                id_user = user.get("id")
                if id_user:
                    arr_users_comments.append((id_user,id_issue))

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