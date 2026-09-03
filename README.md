# 🌱 Smart Fertilizer Recommendation System

An AI-powered full-stack web application that recommends fertilizer type and dosage for farmers based on soil parameters, crop type, environmental conditions, and crop growth stage.

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + TailwindCSS + Recharts |
| Backend | FastAPI + Python 3.11+ |
| Database | SQLite via SQLAlchemy ORM |
| ML Model | RandomForestClassifier (scikit-learn) |
| AI Explanation | Google Gemini 1.5 Flash |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| PDF Reports | ReportLab |

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server (auto-trains model + seeds DB on first launch)
python run.py
```

The backend will be available at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at: `http://localhost:5173`

---   

## 🔐 Authentication

- Register as a **Farmer** to get recommendations
- Register as an **Admin** to access the analytics panel
- JWT tokens are stored in localStorage and auto-attached to requests

---

## 📊 ML Pipeline

On startup, the backend automatically:
1. Generates a synthetic 5,000-row dataset (`ml/fertilizer_data.csv`)
2. Trains a `RandomForestClassifier(n_estimators=200)` 
3. Saves the model as `ml/fertilizer_model.pkl`
4. Loads the model for inference

**Features used for prediction:**
- Nitrogen, Phosphorous, Potassium (soil NPK)
- Temperature, Humidity, Moisture
- Soil Type (inferred from pH)
- Crop Type

**Target:** One of 7 fertilizers: `Urea`, `DAP`, `14-35-14`, `28-28`, `17-17-17`, `20-20`, `10-26-26`

---

## 🌿 Supported Crops

Full growth-stage data (3-4 stages each) for:
| Crop | Stages |
|------|--------|
| Rice (Paddy) | Seedling → Tillering → Panicle Initiation → Ripening |
| Wheat | Germination → Tillering → Jointing → Grain Filling |
| Maize | Seedling → Vegetative → Tasseling → Grain Fill |
| Cotton | Germination → Squaring → Flowering → Boll Development |
| Sugarcane | Germination → Tillering → Grand Growth → Maturation |

---

## 📁 Project Structure

```
FPS/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + lifespan
│   │   ├── config.py        # Settings from .env
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── models/          # ORM models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # ML, Gemini, PDF, Growth Stage
│   │   ├── auth/            # JWT + dependencies
│   │   └── seed/            # Database seeder
│   ├── ml/
│   │   ├── generate_dataset.py
│   │   ├── train_model.py
│   │   ├── evaluate_model.py
│   │   └── fertilizer_model.pkl  (generated)
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    └── src/
        ├── pages/           # Landing, Login, Register, Dashboard, Predict, History, Admin/*
        ├── components/      # Navbar, ProtectedRoute, PredictionResult, Charts
        ├── context/         # AuthContext
        └── api/             # Axios instance
```

---

## 🔗 API Endpoints

### Auth
- `POST /auth/register` — Create account
- `POST /auth/login` — Get JWT token
- `POST /auth/logout` — Client-side logout

### Predictions
- `POST /predict` — Run full ML + Gemini pipeline
- `GET /predict/history` — Current user's history
- `GET /predict/history/{id}` — Single prediction

### Reports
- `GET /reports/{id}/download` — Download PDF report

### Admin (requires admin role)
- `GET /admin/users` — All users
- `GET /admin/predictions` — All predictions
- `GET /admin/analytics` — Dashboard stats
- `GET /admin/model-metrics` — ML metrics + confusion matrix
- `GET/POST/PUT/DELETE /admin/knowledge-base` — CRUD
- `GET/POST/PUT/DELETE /admin/growth-stages` — CRUD

---

## ⚙️ Environment Variables

```env
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=sqlite:///./fertilizer.db
```

---

## 📈 Model Retraining

To retrain the model manually:
```bash
cd backend
python ml/train_model.py
```

To view evaluation metrics only:
```bash
python ml/evaluate_model.py
```

---

> **Disclaimer:** This system provides AI-assisted advisory recommendations. Always consult a certified agronomist for final fertilizer decisions.
