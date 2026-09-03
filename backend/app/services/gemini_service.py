"""
Gemini AI service for natural language fertilizer explanations.
Falls back gracefully if API is unavailable or times out.
"""
import json
import asyncio
import re
from typing import Optional
from app.config import settings

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiService:
    """Service for calling Google Gemini API to get enriched fertilizer recommendations."""

    def __init__(self):
        self._model = None
        self._available = False
        if GENAI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._model = genai.GenerativeModel('gemini-1.5-flash')
                self._available = True
                print("[GeminiService] Initialized with gemini-1.5-flash")
            except Exception as e:
                print(f"[GeminiService] Init failed: {e}")

    def _build_prompt(
        self,
        crop: str,
        predicted_fertilizer: str,
        confidence: float,
        growth_stage: str,
        soil_n: float,
        soil_p: float,
        soil_k: float,
        ph: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        days_since_planting: int,
        stage_notes: str = "",
    ) -> str:
        return f"""You are an expert agricultural scientist specializing in soil science and crop nutrition.

A farmer has submitted the following data for fertilizer recommendation:

**Crop Information:**
- Crop Type: {crop}
- Days Since Planting: {days_since_planting}
- Current Growth Stage: {growth_stage}
- Stage Notes: {stage_notes}

**Soil Parameters:**
- Nitrogen (N): {soil_n} kg/ha
- Phosphorous (P): {soil_p} kg/ha
- Potassium (K): {soil_k} kg/ha
- Soil pH: {ph}

**Environmental Conditions:**
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Rainfall: {rainfall} mm

**ML Model Prediction:**
- Recommended Fertilizer: {predicted_fertilizer}
- Model Confidence: {confidence:.1f}%

Based on this data, provide a comprehensive fertilizer recommendation. Consider the crop's current growth stage and nutritional requirements.

Respond ONLY with a valid JSON object (no markdown, no code fences) in this exact format:
{{
  "refined_fertilizer": "fertilizer name here",
  "dosage_kg_per_acre": 45.0,
  "explanation": "2-3 sentence explanation of why this fertilizer is recommended at this growth stage, considering soil parameters.",
  "alternatives": ["Alternative1", "Alternative2"],
  "application_method": "Brief description of how to apply (broadcast/band/foliar/split)",
  "timing_advice": "Specific advice on when to apply relative to irrigation or weather"
}}"""

    def _parse_response(self, text: str) -> Optional[dict]:
        """Parse JSON from Gemini response, handling markdown code fences."""
        text = text.strip()
        # Remove markdown code fences
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON object with regex
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    return None
        return None

    async def get_recommendation(
        self,
        crop: str,
        predicted_fertilizer: str,
        confidence: float,
        growth_stage: str,
        soil_n: float,
        soil_p: float,
        soil_k: float,
        ph: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        days_since_planting: int,
        stage_notes: str = "",
    ) -> Optional[dict]:
        """
        Call Gemini API for enriched recommendation.
        Returns parsed dict or None on failure (caller uses fallback).
        """
        if not self._available or self._model is None:
            return None

        prompt = self._build_prompt(
            crop, predicted_fertilizer, confidence, growth_stage,
            soil_n, soil_p, soil_k, ph, temperature, humidity,
            rainfall, days_since_planting, stage_notes,
        )

        try:
            # Run in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: self._model.generate_content(prompt)
                ),
                timeout=30.0,
            )
            text = response.text
            result = self._parse_response(text)

            if result and "refined_fertilizer" in result:
                # Validate and clean result
                return {
                    "refined_fertilizer": str(result.get("refined_fertilizer", predicted_fertilizer)),
                    "dosage_kg_per_acre": float(result.get("dosage_kg_per_acre", 40.0)),
                    "explanation": str(result.get("explanation", "")),
                    "alternatives": list(result.get("alternatives", [])),
                    "application_method": str(result.get("application_method", "")),
                    "timing_advice": str(result.get("timing_advice", "")),
                }
            return None

        except asyncio.TimeoutError:
            print("[GeminiService] Request timed out after 30 seconds")
            return None
        except Exception as e:
            print(f"[GeminiService] Error calling API: {e}")
            return None

    def is_available(self) -> bool:
        return self._available


# Module-level singleton
gemini_service = GeminiService()
