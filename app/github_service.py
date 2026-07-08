import requests
from app.config import GITHUB_TOKEN


def get_pull_request_diff(repo_full_name: str, pr_number: int) -> str:
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text


def post_comment_to_pr(repo_full_name: str, pr_number: int, comment: str):
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "body": f"## AI Code Review\n\n{comment}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()
