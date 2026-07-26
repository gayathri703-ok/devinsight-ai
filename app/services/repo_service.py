from sqlalchemy.orm import Session
from app.models.database_models import RepoAnalysis


def create_repo_analysis(db: Session, owner: str, repo: str, full_name: str):
    db_analysis = RepoAnalysis(owner=owner, repo=repo, full_name=full_name)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def get_all_analyses(db: Session):
    return db.query(RepoAnalysis).all()


def get_analysis_by_id(db: Session, analysis_id: int):
    return db.query(RepoAnalysis).filter(RepoAnalysis.id == analysis_id).first()