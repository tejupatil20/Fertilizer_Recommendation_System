"""
Admin router: users, predictions, analytics, model metrics, and CRUD for knowledge base / growth stages.
All routes require admin role.
"""
import json
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.prediction import PredictionHistory
from app.models.knowledge_base import FertilizerKnowledgeBase
from app.models.growth_stages import CropGrowthStage
from app.schemas.auth import UserResponse
from app.schemas.prediction import PredictionResponse, PredictionHistoryItem
from app.schemas.admin import (
    FertilizerKBCreate, FertilizerKBUpdate, FertilizerKBResponse,
    CropGrowthStageCreate, CropGrowthStageUpdate, CropGrowthStageResponse,
    AdminAnalytics, FertilizerCount, CropCount, PredictionOverTime,
)
from app.auth.dependencies import get_current_admin
from app.config import settings

router = APIRouter()


# ---------------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------------

@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """List all registered users."""
    return db.query(User).order_by(User.created_at.desc()).all()


# ---------------------------------------------------------------------------
# PREDICTIONS
# ---------------------------------------------------------------------------

@router.get("/predictions", response_model=List[PredictionHistoryItem])
def list_all_predictions(
    crop: Optional[str] = Query(default=None),
    date_from: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """List all predictions across all users with optional filters."""
    query = db.query(PredictionHistory)

    if crop:
        query = query.filter(PredictionHistory.crop.ilike(f"%{crop}%"))
    if date_from:
        try:
            dt_from = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(PredictionHistory.created_at >= dt_from)
        except ValueError:
            pass
    if date_to:
        try:
            dt_to = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(PredictionHistory.created_at < dt_to)
        except ValueError:
            pass

    return (
        query.order_by(PredictionHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# ---------------------------------------------------------------------------
# MODEL METRICS
# ---------------------------------------------------------------------------

@router.get("/model-metrics")
def get_model_metrics(
    _: User = Depends(get_current_admin),
):
    """Return trained model accuracy metrics and confusion matrix (base64 PNG)."""
    import os
    metrics_path = settings.METRICS_PATH
    if not os.path.exists(metrics_path):
        return {
            "error": "Model metrics not found. Please run model training first.",
            "hint": "Run: python ml/train_model.py from the backend directory",
        }
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    return metrics


# ---------------------------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------------------------

@router.get("/analytics", response_model=AdminAnalytics)
def get_analytics(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """Aggregate stats for admin dashboard."""
    total_predictions = db.query(PredictionHistory).count()
    total_users = db.query(User).count()

    # Most recommended fertilizers
    fertilizer_counts = (
        db.query(
            PredictionHistory.predicted_fertilizer,
            func.count(PredictionHistory.id).label("count"),
        )
        .group_by(PredictionHistory.predicted_fertilizer)
        .order_by(func.count(PredictionHistory.id).desc())
        .limit(7)
        .all()
    )
    most_recommended = [
        FertilizerCount(fertilizer=r.predicted_fertilizer, count=r.count)
        for r in fertilizer_counts
    ]

    # Most queried crops
    crop_counts = (
        db.query(
            PredictionHistory.crop,
            func.count(PredictionHistory.id).label("count"),
        )
        .group_by(PredictionHistory.crop)
        .order_by(func.count(PredictionHistory.id).desc())
        .limit(10)
        .all()
    )
    most_queried_crop = [
        CropCount(crop=r.crop, count=r.count)
        for r in crop_counts
    ]

    # Predictions over last 30 days (SQLite date grouping)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_counts = (
        db.query(
            func.strftime('%Y-%m-%d', PredictionHistory.created_at).label("date"),
            func.count(PredictionHistory.id).label("count"),
        )
        .filter(PredictionHistory.created_at >= thirty_days_ago)
        .group_by(func.strftime('%Y-%m-%d', PredictionHistory.created_at))
        .order_by(func.strftime('%Y-%m-%d', PredictionHistory.created_at))
        .all()
    )
    predictions_over_time = [
        PredictionOverTime(date=r.date, count=r.count)
        for r in daily_counts
    ]

    return AdminAnalytics(
        most_recommended=most_recommended,
        most_queried_crop=most_queried_crop,
        total_predictions=total_predictions,
        total_users=total_users,
        predictions_over_time=predictions_over_time,
    )


# ---------------------------------------------------------------------------
# KNOWLEDGE BASE CRUD
# ---------------------------------------------------------------------------

@router.get("/knowledge-base", response_model=List[FertilizerKBResponse])
def list_knowledge_base(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return db.query(FertilizerKnowledgeBase).order_by(FertilizerKnowledgeBase.fertilizer_name).all()


@router.post("/knowledge-base", response_model=FertilizerKBResponse, status_code=201)
def create_kb_entry(
    data: FertilizerKBCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    existing = db.query(FertilizerKnowledgeBase).filter(
        FertilizerKnowledgeBase.fertilizer_name == data.fertilizer_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Fertilizer entry already exists")
    entry = FertilizerKnowledgeBase(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/knowledge-base/{entry_id}", response_model=FertilizerKBResponse)
def update_kb_entry(
    entry_id: int,
    data: FertilizerKBUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    entry = db.query(FertilizerKnowledgeBase).filter(FertilizerKnowledgeBase.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/knowledge-base/{entry_id}", status_code=204)
def delete_kb_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    entry = db.query(FertilizerKnowledgeBase).filter(FertilizerKnowledgeBase.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# CROP GROWTH STAGES CRUD
# ---------------------------------------------------------------------------

@router.get("/growth-stages", response_model=List[CropGrowthStageResponse])
def list_growth_stages(
    crop: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    query = db.query(CropGrowthStage)
    if crop:
        query = query.filter(CropGrowthStage.crop_name.ilike(f"%{crop}%"))
    return query.order_by(CropGrowthStage.crop_name, CropGrowthStage.min_days).all()


@router.post("/growth-stages", response_model=CropGrowthStageResponse, status_code=201)
def create_growth_stage(
    data: CropGrowthStageCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stage = CropGrowthStage(**data.model_dump())
    db.add(stage)
    db.commit()
    db.refresh(stage)
    return stage


@router.put("/growth-stages/{stage_id}", response_model=CropGrowthStageResponse)
def update_growth_stage(
    stage_id: int,
    data: CropGrowthStageUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stage = db.query(CropGrowthStage).filter(CropGrowthStage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Growth stage not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(stage, field, value)
    db.commit()
    db.refresh(stage)
    return stage


@router.delete("/growth-stages/{stage_id}", status_code=204)
def delete_growth_stage(
    stage_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    stage = db.query(CropGrowthStage).filter(CropGrowthStage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Growth stage not found")
    db.delete(stage)
    db.commit()
    return None
