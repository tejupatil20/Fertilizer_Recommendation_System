"""
ML Service: loads and runs the trained RandomForest fertilizer model.
"""
import os
import joblib
import numpy as np
from typing import Optional, Tuple


SOIL_TYPES = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
CROP_TYPES = ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts']


class MLService:
    """Singleton service for loading and running the fertilizer prediction model."""

    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_encoders: dict = {}
        self.feature_names: list = []
        self.fertilizer_classes: list = []

    def load_model(self, model_path: str) -> bool:
        """Load model bundle from joblib pkl file. Returns True on success."""
        try:
            if not os.path.exists(model_path):
                print(f"[MLService] Model file not found at {model_path}")
                return False
            bundle = joblib.load(model_path)
            self.model = bundle['model']
            self.label_encoder = bundle['label_encoder']
            self.feature_encoders = bundle['feature_encoders']
            self.feature_names = bundle['feature_names']
            self.fertilizer_classes = bundle['fertilizer_classes']
            print(f"[MLService] Model loaded successfully. Classes: {self.fertilizer_classes}")
            return True
        except Exception as e:
            print(f"[MLService] Error loading model: {e}")
            return False

    def _encode_soil_type(self, soil_type: str) -> int:
        """Encode soil type using the fitted LabelEncoder."""
        le = self.feature_encoders.get('Soil Type')
        if le is None:
            return 0
        soil_type = soil_type.strip().title()
        if soil_type not in le.classes_:
            # Find closest match
            soil_type = 'Loamy'
        return int(le.transform([soil_type])[0])

    def _encode_crop_type(self, crop_type: str) -> int:
        """Encode crop type using the fitted LabelEncoder."""
        le = self.feature_encoders.get('Crop Type')
        if le is None:
            return 0
        crop_type = crop_type.strip().title()
        # Handle aliases
        aliases = {
            'Rice': 'Paddy',
            'Ground Nut': 'Ground Nuts',
            'Oilseeds': 'Oil seeds',
        }
        crop_type = aliases.get(crop_type, crop_type)
        if crop_type not in le.classes_:
            # Default to Maize if unknown
            crop_type = le.classes_[0]
        return int(le.transform([crop_type])[0])

    def ph_to_soil_type(self, ph: float) -> str:
        """Infer a rough soil type from pH value."""
        if ph < 5.5:
            return 'Red'
        elif ph < 6.5:
            return 'Sandy'
        elif ph < 7.5:
            return 'Loamy'
        elif ph < 8.5:
            return 'Black'
        else:
            return 'Clayey'

    def humidity_to_moisture(self, humidity: float) -> float:
        """Estimate soil moisture from humidity (rough approximation)."""
        return round(humidity * 0.45, 1)

    def predict(
        self,
        crop: str,
        soil_n: float,
        soil_p: float,
        soil_k: float,
        temperature: float,
        humidity: float,
        ph: float,
        moisture: Optional[float] = None,
        soil_type: Optional[str] = None,
    ) -> Tuple[str, float]:
        """
        Run model prediction.
        Returns (fertilizer_name, confidence_score).
        """
        if not self.is_loaded():
            return ("Urea", 0.5)

        if soil_type is None:
            soil_type = self.ph_to_soil_type(ph)
        if moisture is None:
            moisture = self.humidity_to_moisture(humidity)

        soil_enc = self._encode_soil_type(soil_type)
        crop_enc = self._encode_crop_type(crop)

        # Feature order: ['Nitrogen', 'Phosphorous', 'Potassium', 'Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type']
        X = np.array([[soil_n, soil_p, soil_k, temperature, humidity, moisture, soil_enc, crop_enc]])

        proba = self.model.predict_proba(X)[0]
        pred_class_idx = int(np.argmax(proba))
        confidence = float(proba[pred_class_idx])

        fertilizer_name = self.fertilizer_classes[pred_class_idx]
        return (fertilizer_name, round(confidence * 100, 2))

    def is_loaded(self) -> bool:
        """Check if model is ready for inference."""
        return self.model is not None


# Module-level singleton
ml_service = MLService()
