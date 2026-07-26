from datetime import datetime, timezone
from app.services import github_service


def analyze_activity(owner: str, repo: str) -> dict:
    commits = github_service.fetch_commits(owner, repo, limit=30)
    contributors = github_service.fetch_contributors(owner, repo, limit=30)

    # --- Recency score ---
    recency_score = 0
    days_since_last_commit = None

    if commits:
        last_commit_date_str = commits[0]["commit"]["author"]["date"]
        last_commit_date = datetime.fromisoformat(last_commit_date_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        days_since_last_commit = (now - last_commit_date).days

        if days_since_last_commit <= 30:
            recency_score = 50
        elif days_since_last_commit <= 90:
            recency_score = 30
        elif days_since_last_commit <= 365:
            recency_score = 15
        else:
            recency_score = 0

    # --- Frequency score ---
    commit_count = len(commits)
    if commit_count >= 20:
        frequency_score = 30
    elif commit_count >= 10:
        frequency_score = 20
    elif commit_count >= 1:
        frequency_score = 10
    else:
        frequency_score = 0

    # --- Contributor score ---
    contributor_count = len(contributors)
    if contributor_count >= 10:
        contributor_score = 20
    elif contributor_count >= 3:
        contributor_score = 12
    elif contributor_count >= 1:
        contributor_score = 6
    else:
        contributor_score = 0

    total_score = recency_score + frequency_score + contributor_score

    return {
        "days_since_last_commit": days_since_last_commit,
        "recent_commit_count": commit_count,
        "contributor_count": contributor_count,
        "recency_score": recency_score,
        "frequency_score": frequency_score,
        "contributor_score": contributor_score,
        "activity_score": total_score,
    }

def generate_project_summary(owner: str, repo: str, analysis_data: dict) -> str:
    prompt = f"""You are analyzing the GitHub repository {owner}/{repo}.

Here is the data collected about it:
- Health Score: {analysis_data.get('health_score')}/100
- Documentation: {analysis_data['details']['documentation']}
- Activity: {analysis_data['details']['activity']}
- Code Quality: {analysis_data['details']['code_quality']}
- Popularity: {analysis_data['details']['popularity']}

Write a short, plain-English summary (3-4 sentences) explaining:
1. What this project's overall health looks like
2. Its strongest area
3. Its weakest area
4. One concrete suggestion for improvement

Keep it clear enough for a non-technical person to understand. Do not repeat raw numbers excessively - interpret them."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content