from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class CropGrowthStage(Base):
    __tablename__ = "crop_growth_stages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crop_name = Column(String(50), nullable=False, index=True)
    stage_name = Column(String(100), nullable=False)
    min_days = Column(Integer, nullable=False)
    max_days = Column(Integer, nullable=False)
    recommended_fertilizer = Column(String(100), nullable=True)
    dose_percentage = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
