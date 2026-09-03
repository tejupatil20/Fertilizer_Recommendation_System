"""
Prediction router: full ML pipeline with Gemini enrichment and history.
"""
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.prediction import PredictionHistory
from app.models.knowledge_base import FertilizerKnowledgeBase
from app.schemas.prediction import PredictionInput, PredictionResponse, PredictionHistoryItem
from app.auth.dependencies import get_current_farmer, get_current_user
from app.services.ml_service import ml_service
from app.services.gemini_service import gemini_service
from app.services.growth_stage import get_growth_stage

router = APIRouter()


def build_fallback_explanation(
    fertilizer_name: str,
    growth_stage: str,
    kb_entry,
    soil_n: float,
    soil_p: float,
    soil_k: float,
) -> dict:
    """Build a rule-based explanation when Gemini is unavailable."""
    if kb_entry:
        explanation = (
            f"{fertilizer_name} ({kb_entry.composition or 'balanced NPK'}) is recommended "
            f"for the {growth_stage} stage based on soil analysis showing N={soil_n}, "
            f"P={soil_p}, K={soil_k} kg/ha. {kb_entry.description or ''}"
        )
    else:
        explanation = (
            f"{fertilizer_name} is recommended for the {growth_stage} stage based on "
            f"soil parameters: N={soil_n}, P={soil_p}, K={soil_k} kg/ha. "
            f"Apply as directed by local agricultural guidelines."
        )
    return {
        "refined_fertilizer": fertilizer_name,
        "dosage_kg_per_acre": 40.0,
        "explanation": explanation,
        "alternatives": [],
        "application_method": kb_entry.best_application_stage if kb_entry else "Broadcast or band application",
        "timing_advice": "Apply before irrigation or light rain for best absorption.",
    }


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def predict(
    data: PredictionInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_farmer),
):
    """
    Full fertilizer recommendation pipeline:
    1. Determine growth stage
    2. Run RandomForest ML prediction
    3. Enrich with Gemini AI explanation (with fallback)
    4. Persist to DB
    5. Return combined result
    """
    # Step 1: Growth stage lookup
    growth_stage_obj = get_growth_stage(db, data.crop, data.days_since_planting)
    growth_stage_name = growth_stage_obj.stage_name if growth_stage_obj else "Unknown Stage"
    stage_notes = growth_stage_obj.notes if growth_stage_obj else ""

    # Step 2: ML prediction
    if not ml_service.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model is not loaded. Please contact the administrator.",
        )

    predicted_fertilizer, confidence = ml_service.predict(
        crop=data.crop,
        soil_n=data.soil_n,
        soil_p=data.soil_p,
        soil_k=data.soil_k,
        temperature=data.temperature,
        humidity=data.humidity,
        ph=data.ph,
    )

    # Step 3: Gemini enrichment
    kb_entry = db.query(FertilizerKnowledgeBase).filter(
        FertilizerKnowledgeBase.fertilizer_name.ilike(f"%{predicted_fertilizer}%")
    ).first()

    gemini_result = await gemini_service.get_recommendation(
        crop=data.crop,
        predicted_fertilizer=predicted_fertilizer,
        confidence=confidence,
        growth_stage=growth_stage_name,
        soil_n=data.soil_n,
        soil_p=data.soil_p,
        soil_k=data.soil_k,
        ph=data.ph,
        temperature=data.temperature,
        humidity=data.humidity,
        rainfall=data.rainfall,
        days_since_planting=data.days_since_planting,
        stage_notes=stage_notes,
    )

    # Step 4: Fallback if Gemini fails
    if gemini_result is None:
        gemini_result = build_fallback_explanation(
            predicted_fertilizer, growth_stage_name, kb_entry,
            data.soil_n, data.soil_p, data.soil_k,
        )
        final_fertilizer = predicted_fertilizer
    else:
        final_fertilizer = gemini_result.get("refined_fertilizer", predicted_fertilizer)

    # Step 5: Persist to database
    prediction_record = PredictionHistory(
        user_id=current_user.id,
        crop=data.crop,
        soil_n=data.soil_n,
        soil_p=data.soil_p,
        soil_k=data.soil_k,
        ph=data.ph,
        temperature=data.temperature,
        humidity=data.humidity,
        rainfall=data.rainfall,
        days_since_planting=data.days_since_planting,
        growth_stage=growth_stage_name,
        predicted_fertilizer=final_fertilizer,
        confidence_score=confidence,
        gemini_explanation=gemini_result.get("explanation", ""),
        dosage_kg_per_acre=gemini_result.get("dosage_kg_per_acre"),
        alternatives=json.dumps(gemini_result.get("alternatives", [])),
        application_method=gemini_result.get("application_method", ""),
        timing_advice=gemini_result.get("timing_advice", ""),
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    # Step 6: Return response
    alternatives_list = gemini_result.get("alternatives", [])
    if isinstance(alternatives_list, str):
        try:
            alternatives_list = json.loads(alternatives_list)
        except Exception:
            alternatives_list = []

    return PredictionResponse(
        id=prediction_record.id,
        crop=data.crop,
        soil_n=data.soil_n,
        soil_p=data.soil_p,
        soil_k=data.soil_k,
        ph=data.ph,
        temperature=data.temperature,
        humidity=data.humidity,
        rainfall=data.rainfall,
        days_since_planting=data.days_since_planting,
        growth_stage=growth_stage_name,
        predicted_fertilizer=final_fertilizer,
        confidence_score=confidence,
        gemini_explanation=gemini_result.get("explanation"),
        dosage_kg_per_acre=gemini_result.get("dosage_kg_per_acre"),
        alternatives=alternatives_list,
        application_method=gemini_result.get("application_method"),
        timing_advice=gemini_result.get("timing_advice"),
        created_at=prediction_record.created_at,
    )


@router.get("/predict/history", response_model=List[PredictionHistoryItem])
def get_history(
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get prediction history for the current user."""
    records = (
        db.query(PredictionHistory)
        .filter(PredictionHistory.user_id == current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return records


@router.get("/predict/history/{prediction_id}", response_model=PredictionResponse)
def get_single_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single prediction by ID (must belong to current user or be admin)."""
    record = db.query(PredictionHistory).filter(PredictionHistory.id == prediction_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found")

    if record.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    alternatives_list = []
    if record.alternatives:
        try:
            alternatives_list = json.loads(record.alternatives)
        except Exception:
            alternatives_list = []

    return PredictionResponse(
        id=record.id,
        crop=record.crop,
        soil_n=record.soil_n,
        soil_p=record.soil_p,
        soil_k=record.soil_k,
        ph=record.ph,
        temperature=record.temperature,
        humidity=record.humidity,
        rainfall=record.rainfall,
        days_since_planting=record.days_since_planting,
        growth_stage=record.growth_stage,
        predicted_fertilizer=record.predicted_fertilizer,
        confidence_score=record.confidence_score,
        gemini_explanation=record.gemini_explanation,
        dosage_kg_per_acre=record.dosage_kg_per_acre,
        alternatives=alternatives_list,
        application_method=record.application_method,
        timing_advice=record.timing_advice,
        created_at=record.created_at,
    )
