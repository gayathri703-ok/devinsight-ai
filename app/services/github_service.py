import httpx
import base64
from app.core.config import settings

GITHUB_API_BASE = "https://api.github.com"


def get_headers():
    return {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def fetch_repo_details(owner: str, repo: str):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    response = httpx.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def fetch_repo_languages(owner: str, repo: str):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages"
    response = httpx.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def fetch_contributors(owner: str, repo: str, limit: int = 30):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contributors"
    params = {"per_page": limit}
    response = httpx.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()


def fetch_commits(owner: str, repo: str, limit: int = 30):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    params = {"per_page": limit}
    response = httpx.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()


def fetch_open_issues(owner: str, repo: str, limit: int = 30):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {"state": "open", "per_page": limit}
    response = httpx.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()


def fetch_branches(owner: str, repo: str, limit: int = 30):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/branches"
    params = {"per_page": limit}
    response = httpx.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()


def check_readme_exists(owner: str, repo: str) -> bool:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme"
    response = httpx.get(url, headers=get_headers())
    return response.status_code == 200


def fetch_repo_contents(owner: str, repo: str, path: str = ""):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    response = httpx.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []


def fetch_file_content(owner: str, repo: str, path: str) -> str | None:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    response = httpx.get(url, headers=get_headers())
    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("encoding") == "base64" and data.get("content"):
        try:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        except Exception:
            return None
    return None