# Baseline Audit (29 Oct 2026)

## How to run
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn app.main:app --reload
Docs: http://127.0.0.1:8000/docs
Tests: `pytest` (4 passed)

## Environment
- Python 3.14.3 locally (consider 3.11/3.12 for AI libraries later)
- Secrets: .env is gitignored, never committed, no key rotation needed

## API endpoints
| Method | Path | Purpose | Works? |
|---|---|---|---|
| GET | / | Root status | Yes |
| GET | /health | Health check | |
| GET | /greet/{name} | Demo | |
| GET | /search | Search | |
| POST | /repo-info | Save repo info | |
| GET | /analyses | List saved analyses | |
| GET | /analyses/{analysis_id} | Get one analysis | |
| GET | /github/{owner}/{repo} | Repo metadata | |
| GET | /github/{owner}/{repo}/activity | Activity data | |
| GET | /test-score | Test endpoint | |
| GET | /github/{owner}/{repo}/documentation | Docs analysis | |
| GET | /github/{owner}/{repo}/activity-score | Activity score | |
| GET | /github/{owner}/{repo}/code-quality | Code quality | |
| GET | /github/{owner}/{repo}/popularity | Popularity score | |
| GET | /analyze/{owner}/{repo} | Full analysis | |
| GET | /test-ai | AI test | |
| GET | /github/{owner}/{repo}/security-basic | Basic security | |
| GET | /github/{owner}/{repo}/security-report | Security report | |
| GET | /analyze/{owner}/{repo}/pdf | PDF report | |

## Reusable logic map
| Capability | File | Mixed into route? |
|---|---|---|
| GitHub fetching | github_service.py, repo_service.py | |
| Health score | scoring_service.py + activity/popularity/documentation/code_quality services | |
| Security | security_service.py | |
| Groq summary | ai_service.py | |
| PDF | pdf_service.py | |
| Cache | cache_service.py | |
| Database | core/database.py, models/database_models.py | |

## Observations
- Debug/demo endpoints to remove or hide later: /greet, /search, /test-score, /test-ai
- Route handlers in main.py (e.g. /github/{owner}/{repo}/activity) may contain logic that belongs in services
- Tests only cover scoring_service

## Bugs found
1.

## Not yet present
RAG, agent, MCP, ML (planned)