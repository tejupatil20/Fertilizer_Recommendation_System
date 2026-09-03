from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class FertilizerKnowledgeBase(Base):
    __tablename__ = "fertilizer_knowledge_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fertilizer_name = Column(String(100), unique=True, nullable=False, index=True)
    composition = Column(String(255), nullable=True)
    best_application_stage = Column(String(255), nullable=True)
    precautions = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
