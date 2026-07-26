from app.services import github_service


def analyze_documentation(owner: str, repo: str) -> dict:
    has_readme = github_service.check_readme_exists(owner, repo)
    repo_data = github_service.fetch_repo_details(owner, repo)

    has_license = repo_data.get("license") is not None
    has_wiki = repo_data.get("has_wiki", False)

    score = 0
    if has_readme:
        score += 50
    if has_license:
        score += 30
    if has_wiki:
        score += 20

    return {
        "has_readme": has_readme,
        "has_license": has_license,
        "has_wiki": has_wiki,
        "documentation_score": score,
    }