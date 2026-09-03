"""
Seed data for FertilizerKnowledgeBase and CropGrowthStages.
Called on application startup if tables are empty.
"""
from sqlalchemy.orm import Session
from app.models.knowledge_base import FertilizerKnowledgeBase
from app.models.growth_stages import CropGrowthStage


FERTILIZER_DATA = [
    {
        "fertilizer_name": "Urea",
        "composition": "46% Nitrogen (N)",
        "best_application_stage": "Vegetative / Top-dressing stages",
        "precautions": (
            "Avoid application before heavy rain. Do not apply in standing water. "
            "Split application recommended to avoid nitrogen loss through volatilization. "
            "Keep away from direct contact with seeds."
        ),
        "description": (
            "Urea is the most widely used nitrogenous fertilizer globally. "
            "It provides high nitrogen content and is most effective when incorporated into soil. "
            "Ideal for top-dressing crops that require high nitrogen during vegetative growth."
        ),
    },
    {
        "fertilizer_name": "DAP",
        "composition": "18% Nitrogen (N), 46% Phosphorous (P2O5)",
        "best_application_stage": "Basal application at sowing/transplanting",
        "precautions": (
            "Apply before sowing or at transplanting for best root development. "
            "Avoid mixing with alkaline fertilizers. Store in cool dry place. "
            "Do not over-apply as excess phosphorous can lock out micronutrients."
        ),
        "description": (
            "Di-Ammonium Phosphate (DAP) is a highly concentrated phosphatic fertilizer "
            "with significant nitrogen content. Best suited for basal application to "
            "promote strong root establishment and early crop growth."
        ),
    },
    {
        "fertilizer_name": "14-35-14",
        "composition": "14% N, 35% P2O5, 14% K2O",
        "best_application_stage": "Basal and early vegetative stage",
        "precautions": (
            "Best applied as basal dose before planting. "
            "Avoid applying during drought stress. "
            "Monitor soil pH as high phosphorous can affect pH balance."
        ),
        "description": (
            "A balanced NPK fertilizer with high phosphorous content. "
            "Suitable for crops requiring good root development and balanced early nutrition. "
            "Widely used in vegetable and oilseed crops."
        ),
    },
    {
        "fertilizer_name": "28-28",
        "composition": "28% Nitrogen (N), 28% Phosphorous (P2O5)",
        "best_application_stage": "Basal or early growth stage",
        "precautions": (
            "Apply in split doses for maximum efficiency. "
            "Avoid waterlogging after application. "
            "Combine with potassium fertilizer for complete nutrition."
        ),
        "description": (
            "A high-analysis nitrogen-phosphorous fertilizer. "
            "Provides balanced N and P nutrition for early crop establishment. "
            "Commonly used where potassium levels in soil are already adequate."
        ),
    },
    {
        "fertilizer_name": "17-17-17",
        "composition": "17% N, 17% P2O5, 17% K2O",
        "best_application_stage": "Basal application and first top-dressing",
        "precautions": (
            "Uniform broadcast application recommended. "
            "Avoid contact with foliage. "
            "Supplement with micronutrients for long-duration crops."
        ),
        "description": (
            "A perfectly balanced NPK fertilizer providing equal proportions of all three major nutrients. "
            "Ideal for general-purpose application across a wide range of crops and soil types. "
            "Promotes uniform growth and reduces the risk of nutrient imbalance."
        ),
    },
    {
        "fertilizer_name": "20-20",
        "composition": "20% Nitrogen (N), 20% Phosphorous (P2O5)",
        "best_application_stage": "Basal and tillering stages",
        "precautions": (
            "Use in soils with adequate potassium levels. "
            "Apply before irrigation or rainfall. "
            "Store away from moisture to prevent caking."
        ),
        "description": (
            "A concentrated nitrogen-phosphorous fertilizer suitable for crops grown in "
            "potassium-rich soils. Supports vegetative growth and root development. "
            "Cost-effective for large-scale farming operations."
        ),
    },
    {
        "fertilizer_name": "10-26-26",
        "composition": "10% N, 26% P2O5, 26% K2O",
        "best_application_stage": "Reproductive and grain filling stages",
        "precautions": (
            "Best applied at flowering to grain fill stage. "
            "Avoid excess potassium application in sandy soils. "
            "Monitor crop response and adjust dosage accordingly."
        ),
        "description": (
            "A high phosphorous and potassium fertilizer with moderate nitrogen. "
            "Ideal for crops in reproductive stages requiring strong grain/fruit development. "
            "Promotes flowering, fruit set, and quality improvement."
        ),
    },
    {
        "fertilizer_name": "MOP (Potash)",
        "composition": "60% Potassium (K2O)",
        "best_application_stage": "Basal and later growth stages",
        "precautions": (
            "Avoid application in chloride-sensitive crops like tobacco and some vegetables. "
            "Do not apply to saline soils. "
            "Split application improves uptake efficiency."
        ),
        "description": (
            "Muriate of Potash (MOP) is the primary potassium fertilizer used worldwide. "
            "Strengthens plant cell walls, improves drought tolerance, and enhances crop quality. "
            "Essential for starch and sugar accumulation in roots and tubers."
        ),
    },
]


GROWTH_STAGE_DATA = [
    # Rice
    {"crop_name": "Rice", "stage_name": "Seedling / Nursery", "min_days": 0, "max_days": 20,
     "recommended_fertilizer": "DAP", "dose_percentage": 50,
     "notes": "Apply half dose of DAP as basal before transplanting. Ensure good puddling of field."},
    {"crop_name": "Rice", "stage_name": "Tillering", "min_days": 21, "max_days": 55,
     "recommended_fertilizer": "Urea", "dose_percentage": 25,
     "notes": "First top-dressing with Urea at active tillering (25-30 DAT). Maintain 5cm standing water."},
    {"crop_name": "Rice", "stage_name": "Panicle Initiation", "min_days": 56, "max_days": 90,
     "recommended_fertilizer": "Urea", "dose_percentage": 25,
     "notes": "Second top-dressing at panicle initiation. Apply 10-26-26 if K is needed. Drain field before application."},
    {"crop_name": "Rice", "stage_name": "Ripening / Maturity", "min_days": 91, "max_days": 135,
     "recommended_fertilizer": "MOP (Potash)", "dose_percentage": 0,
     "notes": "Avoid nitrogen at ripening stage. Apply potash if flag leaf shows deficiency. Allow field to dry."},

    # Wheat
    {"crop_name": "Wheat", "stage_name": "Germination / Establishment", "min_days": 0, "max_days": 15,
     "recommended_fertilizer": "DAP", "dose_percentage": 50,
     "notes": "Apply DAP as basal at sowing. Ensure good seed-soil contact. Use 100-120 kg/ha DAP."},
    {"crop_name": "Wheat", "stage_name": "Tillering", "min_days": 16, "max_days": 45,
     "recommended_fertilizer": "Urea", "dose_percentage": 50,
     "notes": "Top-dress with Urea at crown root initiation (21 DAS). Irrigate immediately after application."},
    {"crop_name": "Wheat", "stage_name": "Jointing / Booting", "min_days": 46, "max_days": 70,
     "recommended_fertilizer": "20-20", "dose_percentage": 25,
     "notes": "Apply second dose of nitrogen at jointing stage. Critical stage for tiller production and grain number."},
    {"crop_name": "Wheat", "stage_name": "Grain Filling / Dough", "min_days": 71, "max_days": 110,
     "recommended_fertilizer": "MOP (Potash)", "dose_percentage": 0,
     "notes": "Foliar spray of 2% urea at grain filling if yellowing observed. Ensure adequate moisture for grain development."},

    # Maize
    {"crop_name": "Maize", "stage_name": "Seedling (V1-V4)", "min_days": 0, "max_days": 20,
     "recommended_fertilizer": "17-17-17", "dose_percentage": 33,
     "notes": "Apply basal NPK at sowing. Ensure phosphorous is banded near seed row for good root development."},
    {"crop_name": "Maize", "stage_name": "Vegetative (V5-V12)", "min_days": 21, "max_days": 50,
     "recommended_fertilizer": "Urea", "dose_percentage": 33,
     "notes": "Side-dress Urea at V5-V6 stage. Critical period for ear development begins at V6. Avoid N deficiency."},
    {"crop_name": "Maize", "stage_name": "Tasseling / Silking (VT-R1)", "min_days": 51, "max_days": 75,
     "recommended_fertilizer": "Urea", "dose_percentage": 34,
     "notes": "Final nitrogen application before tasseling. Most critical stage — drought or nutrient stress reduces yield significantly."},
    {"crop_name": "Maize", "stage_name": "Grain Fill / Maturity (R2-R6)", "min_days": 76, "max_days": 110,
     "recommended_fertilizer": "10-26-26", "dose_percentage": 0,
     "notes": "No additional N needed. Ensure adequate K and P for starch accumulation. Maintain soil moisture."},

    # Cotton
    {"crop_name": "Cotton", "stage_name": "Germination / Seedling", "min_days": 0, "max_days": 25,
     "recommended_fertilizer": "DAP", "dose_percentage": 25,
     "notes": "Apply basal DAP and MOP before sowing. Avoid excess N at this stage to prevent vegetative overgrowth."},
    {"crop_name": "Cotton", "stage_name": "Squaring (Flower Bud Formation)", "min_days": 26, "max_days": 65,
     "recommended_fertilizer": "Urea", "dose_percentage": 50,
     "notes": "First top-dressing at 30-35 DAS. Critical for boll set. Ensure adequate moisture and potassium."},
    {"crop_name": "Cotton", "stage_name": "Flowering / Boll Setting", "min_days": 66, "max_days": 105,
     "recommended_fertilizer": "20-20", "dose_percentage": 25,
     "notes": "Second top-dressing at first flowering. Boron spray (0.2%) recommended to improve boll retention."},
    {"crop_name": "Cotton", "stage_name": "Boll Development / Maturity", "min_days": 106, "max_days": 170,
     "recommended_fertilizer": "MOP (Potash)", "dose_percentage": 0,
     "notes": "Apply K2O to improve fiber quality and boll weight. Reduce irrigation as bolls mature for better opening."},

    # Sugarcane
    {"crop_name": "Sugarcane", "stage_name": "Germination / Establishment", "min_days": 0, "max_days": 35,
     "recommended_fertilizer": "DAP", "dose_percentage": 25,
     "notes": "Apply basal dose (DAP + MOP) in furrows before planting. Critical stage for root establishment and early shoot emergence."},
    {"crop_name": "Sugarcane", "stage_name": "Tillering", "min_days": 36, "max_days": 100,
     "recommended_fertilizer": "Urea", "dose_percentage": 25,
     "notes": "First top-dressing at 45-60 days. Side-dress Urea along rows. Critical for maximum tiller production."},
    {"crop_name": "Sugarcane", "stage_name": "Grand Growth (Elongation)", "min_days": 101, "max_days": 240,
     "recommended_fertilizer": "Urea", "dose_percentage": 50,
     "notes": "Major nitrogen application during grand growth. Apply in 2 splits (120 and 150 days). Ensure adequate irrigation."},
    {"crop_name": "Sugarcane", "stage_name": "Maturation / Ripening", "min_days": 241, "max_days": 360,
     "recommended_fertilizer": "MOP (Potash)", "dose_percentage": 0,
     "notes": "Stop nitrogen application 2 months before harvest. Potash improves sucrose content. Allow ripening without excessive irrigation."},
]


def seed_database(db: Session) -> None:
    """Seed the database with initial fertilizer and growth stage data (idempotent)."""
    # Seed FertilizerKnowledgeBase
    if db.query(FertilizerKnowledgeBase).count() == 0:
        for entry in FERTILIZER_DATA:
            kb = FertilizerKnowledgeBase(**entry)
            db.add(kb)
        db.commit()
        print(f"[Seed] Seeded {len(FERTILIZER_DATA)} fertilizer knowledge base entries.")
    else:
        print("[Seed] Fertilizer knowledge base already seeded, skipping.")

    # Seed CropGrowthStages
    if db.query(CropGrowthStage).count() == 0:
        for entry in GROWTH_STAGE_DATA:
            stage = CropGrowthStage(**entry)
            db.add(stage)
        db.commit()
        print(f"[Seed] Seeded {len(GROWTH_STAGE_DATA)} crop growth stage entries.")
    else:
        print("[Seed] Crop growth stages already seeded, skipping.")
