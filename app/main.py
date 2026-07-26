from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.models import database_models
from app.models.schemas import RepoRequest, RepoResponse, GitHubRepoResponse, AnalyzeResponse
from app.services import repo_service
from app.services import github_service
from app.services import scoring_service
from app.services import documentation_service
from app.services import activity_service
from app.services import code_quality_service
from app.services import popularity_service
from app.services import analysis_service
from app.services import ai_service
from app.services import security_service
from app.services import pdf_service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevInsight AI",
    description="Analyze GitHub repositories and generate a Repository Health Score.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "DevInsight AI is running", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to DevInsight AI."}


@app.get("/search")
def search_repos(keyword: str, limit: int = 5):
    return {
        "keyword": keyword,
        "limit": limit,
        "message": f"Searching for repos matching '{keyword}', showing top {limit} results."
    }


@app.post("/repo-info", response_model=RepoResponse)
def get_repo_info(data: RepoRequest, db: Session = Depends(get_db)):
    saved = repo_service.create_repo_analysis(
        db=db, owner=data.owner, repo=data.repo, full_name=f"{data.owner}/{data.repo}"
    )
    return RepoResponse(
        owner=saved.owner,
        repo=saved.repo,
        full_name=saved.full_name,
        message="Repository info saved to database successfully."
    )


@app.get("/analyses")
def list_analyses(db: Session = Depends(get_db)):
    return repo_service.get_all_analyses(db)


@app.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    return repo_service.get_analysis_by_id(db, analysis_id)


@app.get("/github/{owner}/{repo}", response_model=GitHubRepoResponse)
def get_github_repo(owner: str, repo: str):
    data = github_service.fetch_repo_details(owner, repo)
    languages = github_service.fetch_repo_languages(owner, repo)

    return GitHubRepoResponse(
        name=data.get("name"),
        owner=data.get("owner", {}).get("login"),
        stars=data.get("stargazers_count"),
        forks=data.get("forks_count"),
        watchers=data.get("watchers_count"),
        primary_language=data.get("language"),
        description=data.get("description"),
        languages=languages,
    )


@app.get("/github/{owner}/{repo}/activity")
def get_repo_activity(owner: str, repo: str):
    contributors = github_service.fetch_contributors(owner, repo)
    commits = github_service.fetch_commits(owner, repo)
    issues = github_service.fetch_open_issues(owner, repo)
    branches = github_service.fetch_branches(owner, repo)

    return {
        "contributor_count": len(contributors),
        "top_contributors": [c["login"] for c in contributors[:5]],
        "recent_commit_count": len(commits),
        "latest_commit_message": commits[0]["commit"]["message"] if commits else None,
        "open_issue_count": len(issues),
        "branch_count": len(branches),
        "branch_names": [b["name"] for b in branches],
    }


@app.get("/test-score")
def test_score():
    fake_scores = {
        "documentation": 80,
        "activity": 90,
        "testing": 40,
        "code_structure": 70,
        "popularity": 100,
        "security": 60,
    }
    return scoring_service.calculate_health_score(fake_scores)


@app.get("/github/{owner}/{repo}/documentation")
def get_documentation_analysis(owner: str, repo: str):
    return documentation_service.analyze_documentation(owner, repo)


@app.get("/github/{owner}/{repo}/activity-score")
def get_activity_analysis(owner: str, repo: str):
    return activity_service.analyze_activity(owner, repo)


@app.get("/github/{owner}/{repo}/code-quality")
def get_code_quality_analysis(owner: str, repo: str):
    return code_quality_service.analyze_code_quality(owner, repo)


@app.get("/github/{owner}/{repo}/popularity")
def get_popularity_analysis(owner: str, repo: str):
    return popularity_service.analyze_popularity(owner, repo)


@app.get("/analyze/{owner}/{repo}", response_model=AnalyzeResponse)
def analyze_repo(owner: str, repo: str, db: Session = Depends(get_db)):
    result = analysis_service.analyze_repository(owner, repo)
    repo_service.create_repo_analysis(
        db=db, owner=owner, repo=repo, full_name=f"{owner}/{repo}"
    )
    return result


@app.get("/test-ai")
def test_ai_connection():
    return {"response": ai_service.test_connection()}


@app.get("/github/{owner}/{repo}/security-basic")
def get_basic_security_checks(owner: str, repo: str):
    return security_service.run_basic_security_checks(owner, repo)


@app.get("/github/{owner}/{repo}/security-report")
def get_security_report(owner: str, repo: str):
    return security_service.generate_security_report(owner, repo)


@app.get("/analyze/{owner}/{repo}/pdf")
def download_pdf_report(owner: str, repo: str):
    analysis_data = analysis_service.analyze_repository(owner, repo)
    pdf_bytes = pdf_service.generate_pdf_report(analysis_data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={owner}-{repo}-report.pdf"},
    )