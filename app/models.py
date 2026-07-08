from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    commit_sha = Column(String, nullable=True)
    diff_text = Column(Text, nullable=False)
    review_result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
