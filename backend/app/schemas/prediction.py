from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PredictionInput(BaseModel):
    crop: str = Field(..., description="Crop type")
    soil_n: float = Field(..., ge=0, le=140, description="Soil Nitrogen (kg/ha)")
    soil_p: float = Field(..., ge=0, le=145, description="Soil Phosphorous (kg/ha)")
    soil_k: float = Field(..., ge=0, le=205, description="Soil Potassium (kg/ha)")
    ph: float = Field(..., ge=0, le=14, description="Soil pH")
    temperature: float = Field(..., description="Temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Humidity (%)")
    rainfall: float = Field(..., ge=0, description="Rainfall (mm)")
    days_since_planting: int = Field(..., ge=0, description="Days since planting")


class PredictionResponse(BaseModel):
    id: int
    crop: str
    soil_n: float
    soil_p: float
    soil_k: float
    ph: float
    temperature: float
    humidity: float
    rainfall: float
    days_since_planting: int
    growth_stage: Optional[str] = None
    predicted_fertilizer: str
    confidence_score: float
    gemini_explanation: Optional[str] = None
    dosage_kg_per_acre: Optional[float] = None
    alternatives: Optional[List[str]] = None
    application_method: Optional[str] = None
    timing_advice: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PredictionHistoryItem(BaseModel):
    id: int
    crop: str
    predicted_fertilizer: str
    confidence_score: float
    growth_stage: Optional[str] = None
    dosage_kg_per_acre: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
