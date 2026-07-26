from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class RepoAnalysis(Base):
    __tablename__ = "repo_analyses"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    repo = Column(String, index=True)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)