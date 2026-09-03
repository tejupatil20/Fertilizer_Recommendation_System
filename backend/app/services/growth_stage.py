"""
Growth stage lookup service.
"""
from sqlalchemy.orm import Session
from app.models.growth_stages import CropGrowthStage
from typing import Optional


def get_growth_stage(db: Session, crop_name: str, days: int) -> Optional[CropGrowthStage]:
    """
    Look up the growth stage for a given crop and number of days since planting.
    Case-insensitive crop name matching.
    """
    # Handle Rice/Paddy alias
    aliases = {
        "rice": "paddy",
        "paddy": "paddy",
        "maize": "maize",
        "corn": "maize",
        "wheat": "wheat",
        "cotton": "cotton",
        "sugarcane": "sugarcane",
    }
    crop_lower = crop_name.lower().strip()
    normalized = aliases.get(crop_lower, crop_lower)

    stage = (
        db.query(CropGrowthStage)
        .filter(
            CropGrowthStage.crop_name.ilike(f"%{normalized}%"),
            CropGrowthStage.min_days <= days,
            CropGrowthStage.max_days >= days,
        )
        .first()
    )

    # If no exact match, try by crop name only and return last stage
    if stage is None:
        stage = (
            db.query(CropGrowthStage)
            .filter(CropGrowthStage.crop_name.ilike(f"%{normalized}%"))
            .order_by(CropGrowthStage.max_days.desc())
            .first()
        )

    return stage


def get_all_stages_for_crop(db: Session, crop_name: str) -> list[CropGrowthStage]:
    """Return all growth stages for a crop, ordered by min_days."""
    aliases = {
        "rice": "Rice",
        "paddy": "Rice",
        "maize": "Maize",
        "corn": "Maize",
        "wheat": "Wheat",
        "cotton": "Cotton",
        "sugarcane": "Sugarcane",
    }
    crop_lower = crop_name.lower().strip()
    normalized_title = aliases.get(crop_lower, crop_name.title())

    return (
        db.query(CropGrowthStage)
        .filter(CropGrowthStage.crop_name.ilike(f"%{normalized_title}%"))
        .order_by(CropGrowthStage.min_days)
        .all()
    )
