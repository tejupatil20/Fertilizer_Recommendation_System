"""
Reports router: download PDF report for a prediction.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database import get_db
from app.models.user import User
from app.models.prediction import PredictionHistory
from app.models.knowledge_base import FertilizerKnowledgeBase
from app.auth.dependencies import get_current_user
from app.services.report_service import generate_prediction_report
from app.services.growth_stage import get_all_stages_for_crop

router = APIRouter()


@router.get("/reports/{prediction_id}/download")
def download_report(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate and download a PDF report for a given prediction ID."""
    # Fetch prediction
    prediction = db.query(PredictionHistory).filter(
        PredictionHistory.id == prediction_id
    ).first()

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Authorization check
    if prediction.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    # Fetch the user who made the prediction
    prediction_user = db.query(User).filter(User.id == prediction.user_id).first()
    if not prediction_user:
        prediction_user = current_user

    # Fetch all growth stages for this crop
    growth_stages = get_all_stages_for_crop(db, prediction.crop)

    # Fetch knowledge base entry for this fertilizer
    kb_entry = db.query(FertilizerKnowledgeBase).filter(
        FertilizerKnowledgeBase.fertilizer_name.ilike(
            f"%{prediction.predicted_fertilizer}%"
        )
    ).first()

    # Generate PDF
    try:
        pdf_bytes = generate_prediction_report(
            prediction=prediction,
            user=prediction_user,
            growth_stages=growth_stages,
            knowledge_base_entry=kb_entry,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF report: {str(e)}"
        )

    filename = f"fertilizer_report_{prediction_id}_{prediction.crop.lower()}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )
