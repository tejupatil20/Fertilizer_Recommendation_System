from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crop = Column(String(50), nullable=False)
    soil_n = Column(Float, nullable=False)
    soil_p = Column(Float, nullable=False)
    soil_k = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    days_since_planting = Column(Integer, nullable=False)
    growth_stage = Column(String(100), nullable=True)
    predicted_fertilizer = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    gemini_explanation = Column(String(2000), nullable=True)
    dosage_kg_per_acre = Column(Float, nullable=True)
    alternatives = Column(String(500), nullable=True)   # JSON-encoded list
    application_method = Column(String(500), nullable=True)
    timing_advice = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
