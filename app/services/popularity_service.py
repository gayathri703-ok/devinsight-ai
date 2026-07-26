import math
from app.services import github_service


def _log_scale_score(value: int, max_expected: int, max_points: int) -> float:
    """
    Scores a value on a logarithmic curve.
    max_expected = the value considered 'excellent' (scores near max_points)
    """
    if value <= 0:
        return 0
    score = (math.log10(value + 1) / math.log10(max_expected + 1)) * max_points
    return min(round(score, 2), max_points)


def analyze_popularity(owner: str, repo: str) -> dict:
    data = github_service.fetch_repo_details(owner, repo)

    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    watchers = data.get("watchers_count", 0)

    star_score = _log_scale_score(stars, max_expected=50000, max_points=50)
    fork_score = _log_scale_score(forks, max_expected=10000, max_points=30)
    watcher_score = _log_scale_score(watchers, max_expected=5000, max_points=20)

    total_score = round(star_score + fork_score + watcher_score, 2)

    return {
        "stars": stars,
        "forks": forks,
        "watchers": watchers,
        "star_score": star_score,
        "fork_score": fork_score,
        "watcher_score": watcher_score,
        "popularity_score": min(total_score, 100),
    }