from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FertilizerKBCreate(BaseModel):
    fertilizer_name: str
    composition: Optional[str] = None
    best_application_stage: Optional[str] = None
    precautions: Optional[str] = None
    description: Optional[str] = None


class FertilizerKBUpdate(BaseModel):
    fertilizer_name: Optional[str] = None
    composition: Optional[str] = None
    best_application_stage: Optional[str] = None
    precautions: Optional[str] = None
    description: Optional[str] = None


class FertilizerKBResponse(BaseModel):
    id: int
    fertilizer_name: str
    composition: Optional[str] = None
    best_application_stage: Optional[str] = None
    precautions: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CropGrowthStageCreate(BaseModel):
    crop_name: str
    stage_name: str
    min_days: int
    max_days: int
    recommended_fertilizer: Optional[str] = None
    dose_percentage: Optional[int] = None
    notes: Optional[str] = None


class CropGrowthStageUpdate(BaseModel):
    crop_name: Optional[str] = None
    stage_name: Optional[str] = None
    min_days: Optional[int] = None
    max_days: Optional[int] = None
    recommended_fertilizer: Optional[str] = None
    dose_percentage: Optional[int] = None
    notes: Optional[str] = None


class CropGrowthStageResponse(BaseModel):
    id: int
    crop_name: str
    stage_name: str
    min_days: int
    max_days: int
    recommended_fertilizer: Optional[str] = None
    dose_percentage: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class FertilizerCount(BaseModel):
    fertilizer: str
    count: int


class CropCount(BaseModel):
    crop: str
    count: int


class PredictionOverTime(BaseModel):
    date: str
    count: int


class AdminAnalytics(BaseModel):
    most_recommended: List[FertilizerCount]
    most_queried_crop: List[CropCount]
    total_predictions: int
    total_users: int
    predictions_over_time: List[PredictionOverTime]
