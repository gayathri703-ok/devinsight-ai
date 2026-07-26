from pydantic import BaseModel, Field


class RepoRequest(BaseModel):
    owner: str = Field(..., description="GitHub username or organization")
    repo: str = Field(..., description="Repository name")


class RepoResponse(BaseModel):
    owner: str
    repo: str
    full_name: str
    message: str


class GitHubRepoResponse(BaseModel):
    name: str
    owner: str
    stars: int
    forks: int
    watchers: int
    primary_language: str | None
    description: str | None
    languages: dict[str, int]


class CategoryBreakdown(BaseModel):
    raw_score: float
    weight: int
    contribution: float


class HealthScoreBreakdown(BaseModel):
    documentation: CategoryBreakdown
    activity: CategoryBreakdown
    testing: CategoryBreakdown
    code_structure: CategoryBreakdown
    popularity: CategoryBreakdown
    security: CategoryBreakdown


class AISummary(BaseModel):
    overview: str
    tech_stack_explanation: str
    strongest_area: str
    weakest_area: str
    improvement_suggestions: list[str]


class AnalyzeResponse(BaseModel):
    owner: str
    repo: str
    health_score: float
    breakdown: HealthScoreBreakdown
    ai_summary: AISummary
    details: dict