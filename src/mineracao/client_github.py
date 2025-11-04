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