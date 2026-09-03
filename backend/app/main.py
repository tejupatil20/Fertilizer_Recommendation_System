"""
FastAPI application entry point.
Handles startup (DB init, seed, model training/loading) and CORS configuration.
"""
import os
import sys
import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, SessionLocal
from app.seed.seed_data import seed_database
from app.services.ml_service import ml_service
from app.routers import auth, predict, reports, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup → yield → shutdown."""
    print("[Startup] Initializing Smart Fertilizer Recommendation System...")

    # 1. Create database tables
    init_db()
    print("[Startup] Database tables created/verified.")

    # 2. Seed database with initial data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    # 3. Train model if not found, then load it
    model_path = settings.MODEL_PATH
    if not os.path.exists(model_path):
        print(f"[Startup] Model not found at '{model_path}'. Training now...")
        try:
            # Run training script as subprocess from backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            result = subprocess.run(
                [sys.executable, "ml/train_model.py"],
                cwd=backend_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                print("[Startup] Model training completed successfully.")
                print(result.stdout)
            else:
                print(f"[Startup] Model training failed:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            print("[Startup] Model training timed out after 5 minutes.")
        except Exception as e:
            print(f"[Startup] Could not run training: {e}")

    # 4. Load model into memory
    if os.path.exists(model_path):
        success = ml_service.load_model(model_path)
        if success:
            print("[Startup] ✅ ML Model loaded and ready.")
        else:
            print("[Startup] ⚠️  ML Model load failed. Predictions will return fallback values.")
    else:
        print("[Startup] ⚠️  Model file still not found. Check ml/train_model.py.")

    print("[Startup] 🚀 Server is ready!")
    yield
    print("[Shutdown] Shutting down gracefully.")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "AI-powered fertilizer recommendation system using RandomForest ML + Gemini AI. "
        "Provides crop-specific fertilizer recommendations based on soil parameters."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(predict.router, tags=["Predictions"])
app.include_router(reports.router, tags=["Reports"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": ml_service.is_loaded(),
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Smart Fertilizer Recommendation System API",
        "docs": "/docs",
        "health": "/health",
    }
