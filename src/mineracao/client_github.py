import os
import requests

class GithubClient:
    URLBASE = "https://api.github.com/repos/sorrycc/awesome-javascript"

    def __init__(self):
        auth_token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization" : f"Bearer {auth_token}"
        }


    def getIssues(self):
        ulrBusca = f"{GithubClient.URLBASE}/issues";
        return requests.get(url=ulrBusca, headers=self.headers).json();

    def getIssuesComments(self):
        ulrBusca = f"{GithubClient.URLBASE}/issues/comments";
        return requests.get(url=ulrBusca, headers=self.headers).json();

    def getIssueComments(self, issueId: str):
        urlBusca = f"{GithubClient.URLBASE}/issues/{issueId}/comments";
        return requests.get(url=urlBusca, headers=self.headers).json();

    def getClosedIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues";
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json();

    def getOpenIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues";
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json();

    def getOpenPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls";
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json();

    def getClosedPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls";
        return requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json();

    def getMergedPullRequests(self):
        urlBusca = f"{GithubClient.URLBASE}/pulls";
        arr_pulls = requests.get(url=urlBusca, headers=self.headers, params={"state": "all"}).json();
        arr_pulls_merged = [];

        for pull in arr_pulls:
            if pull["merged_at"]:
                arr_pulls_merged.append(pull);

        return arr_pulls_merged

    def getUsersFromOpenIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues";
        arr_issues = requests.get(url=urlBusca, headers=self.headers, params={"state": "open"}).json();

        arr_users = [];
        for issue in arr_issues:
            assignee = issue.get("user")

            if assignee:
                login = assignee.get("login")
                if login:
                    arr_users.append(login)

        return arr_users;

    def getUsersFromClosedIssues(self):
        urlBusca = f"{GithubClient.URLBASE}/issues";
        arr_issues = requests.get(url=urlBusca, headers=self.headers, params={"state": "closed"}).json();

        arr_users = [];
        for issue in arr_issues:
            assignee = issue.get("user")

            if assignee:
                login = assignee.get("login")
                if login:
                    arr_users.append(login)

        return arr_users;