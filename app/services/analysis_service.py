from app.services import documentation_service
from app.services import activity_service
from app.services import code_quality_service
from app.services import popularity_service
from app.services import scoring_service
from app.services import ai_service
from app.services import github_service
from app.services import cache_service
from app.services import security_service


def analyze_repository(owner: str, repo: str) -> dict:
    cache_key = f"{owner}/{repo}"
    cached_result = cache_service.get_cached(cache_key)
    if cached_result is not None:
        return cached_result

    documentation = documentation_service.analyze_documentation(owner, repo)
    activity = activity_service.analyze_activity(owner, repo)
    code_quality = code_quality_service.analyze_code_quality(owner, repo)
    popularity = popularity_service.analyze_popularity(owner, repo)

    category_scores = {
        "documentation": documentation["documentation_score"],
        "activity": activity["activity_score"],
        "testing": code_quality["code_quality_score"],
        "code_structure": code_quality["code_quality_score"],
        "popularity": popularity["popularity_score"],
        "security": security_service.calculate_security_score([
            security_service.check_missing_readme(owner, repo),
            security_service.check_missing_license(owner, repo),
            security_service.check_large_files(owner, repo),
            security_service.check_sensitive_filenames(owner, repo),
            security_service.check_exposed_secrets(owner, repo),
        ]),
    }

    health_result = scoring_service.calculate_health_score(category_scores)

    github_data = github_service.fetch_repo_details(owner, repo)
    languages = github_service.fetch_repo_languages(owner, repo)

    ai_summary = ai_service.generate_project_summary(owner, repo, {
        "health_score": health_result["health_score"],
        "primary_language": github_data.get("language"),
        "languages": languages,
        "details": {
            "documentation": documentation,
            "activity": activity,
            "code_quality": code_quality,
            "popularity": popularity,
        }
    })

    result = {
        "owner": owner,
        "repo": repo,
        "health_score": health_result["health_score"],
        "breakdown": health_result["breakdown"],
        "ai_summary": ai_summary,
        "details": {
            "documentation": documentation,
            "activity": activity,
            "code_quality": code_quality,
            "popularity": popularity,
        },
    }

    cache_service.set_cached(cache_key, result)
    return result