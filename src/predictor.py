"""Runtime prediction helpers for PlantDiseaseDetector."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

from src.model import CLASS_NAMES, IMAGE_SIZE

DISEASE_INFO = {
    "Pepper__bell___Bacterial_spot": {
        "description": "Bacterial spot causes small water-soaked lesions that darken on pepper leaves and fruit.",
        "treatment": "Remove infected debris, avoid overhead watering, improve spacing, and apply copper-based bactericide according to label directions.",
        "severity": "Moderate",
    },
    "Pepper__bell___healthy": {
        "description": "The bell pepper leaf appears healthy with no visible disease symptoms.",
        "treatment": "No treatment is needed. Continue balanced watering, nutrition, and routine scouting.",
        "severity": "None",
    },
    "Potato___Early_blight": {
        "description": "Early blight is a fungal disease that often forms dark concentric rings on older potato leaves.",
        "treatment": "Remove affected foliage, rotate crops, mulch to reduce soil splash, and use a labeled fungicide such as chlorothalonil or mancozeb when pressure is high.",
        "severity": "Moderate",
    },
    "Potato___Late_blight": {
        "description": "Late blight is a fast-spreading disease that creates water-soaked lesions and can destroy potato plants quickly.",
        "treatment": "Act quickly: remove and destroy infected plants, avoid overhead irrigation, and apply a labeled late-blight fungicide program.",
        "severity": "High",
    },
    "Potato___healthy": {
        "description": "The potato leaf appears healthy with no visible disease symptoms.",
        "treatment": "No treatment is needed. Maintain good airflow, watering discipline, and regular monitoring.",
        "severity": "None",
    },
    "Tomato_Bacterial_spot": {
        "description": "Bacterial spot causes small dark spots on tomato leaves, stems, and fruit, especially in warm wet conditions.",
        "treatment": "Remove infected debris, avoid handling wet plants, use disease-free seed or transplants, and apply copper-based products when appropriate.",
        "severity": "Moderate",
    },
    "Tomato_Early_blight": {
        "description": "Early blight causes target-like brown lesions, commonly starting on older tomato leaves.",
        "treatment": "Prune infected lower leaves, stake or mulch plants, rotate crops, and apply a labeled fungicide if disease continues spreading.",
        "severity": "Moderate",
    },
    "Tomato_Late_blight": {
        "description": "Late blight causes large dark lesions and can rapidly collapse tomato foliage and fruit.",
        "treatment": "Remove infected plants, dispose of debris away from the garden, avoid overhead irrigation, and begin a labeled fungicide program immediately.",
        "severity": "High",
    },
    "Tomato_Leaf_Mold": {
        "description": "Leaf mold produces yellow patches on upper leaf surfaces and fuzzy mold growth on the underside.",
        "treatment": "Increase ventilation, reduce humidity, avoid wetting leaves, remove infected foliage, and apply a labeled fungicide if needed.",
        "severity": "Moderate",
    },
    "Tomato_Septoria_leaf_spot": {
        "description": "Septoria leaf spot causes many small circular lesions with pale centers and dark margins on tomato leaves.",
        "treatment": "Remove infected leaves, mulch to reduce soil splash, rotate crops, and apply a labeled protectant fungicide during wet periods.",
        "severity": "Moderate",
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "description": "Two-spotted spider mites cause stippling, yellowing, and fine webbing on tomato foliage.",
        "treatment": "Rinse leaf undersides, reduce plant stress, use insecticidal soap or horticultural oil, and consider predatory mites for persistent infestations.",
        "severity": "Moderate",
    },
    "Tomato__Target_Spot": {
        "description": "Target spot is a fungal disease that creates brown lesions with concentric rings on tomato leaves.",
        "treatment": "Remove infected foliage, improve airflow, avoid overhead watering, clean up plant debris, and apply a labeled fungicide when needed.",
        "severity": "Moderate",
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "description": "Tomato yellow leaf curl virus causes yellowing, upward leaf curling, stunting, and reduced fruit set.",
        "treatment": "There is no cure. Remove infected plants, control whiteflies, manage weeds, and use resistant tomato varieties.",
        "severity": "High",
    },
    "Tomato__Tomato_mosaic_virus": {
        "description": "Tomato mosaic virus causes mottled mosaic patterns, curling, distortion, and uneven growth.",
        "treatment": "There is no cure. Remove infected plants, disinfect tools, wash hands after handling plants, and use resistant varieties.",
        "severity": "High",
    },
    "Tomato_healthy": {
        "description": "The tomato leaf appears healthy with no visible disease symptoms.",
        "treatment": "No treatment is needed. Continue regular care and monitor for early signs of pests or disease.",
        "severity": "None",
    },
}


class PlantDiseasePredictor:
    """Load a trained Keras model and produce enriched disease predictions."""

    def __init__(self, model_path: str = "models/plant_disease_model.keras") -> None:
        self.model_path = model_path
        self.model: tf.keras.Model | None = None

    def load(self) -> None:
        """Load the saved model from disk."""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = tf.keras.models.load_model(self.model_path)

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Convert raw image bytes into a 256x256 normalized float32 RGB array."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError("Uploaded file is not a valid image.") from exc

        image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
        image_array = np.asarray(image, dtype=np.float32) / 255.0
        return image_array.astype(np.float32)

    def predict(self, image_bytes: bytes) -> dict[str, Any]:
        """Run inference and return class, confidence, disease info, and top-3 predictions."""
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        image_array = self.preprocess_image(image_bytes)
        batch = np.expand_dims(image_array, axis=0)
        predictions = self.model.predict(batch, verbose=0)[0]

        predicted_index = int(np.argmax(predictions))
        predicted_class = CLASS_NAMES[predicted_index]
        confidence = round(float(predictions[predicted_index]) * 100, 2)
        disease_info = DISEASE_INFO[predicted_class]

        top3_indices = np.argsort(predictions)[::-1][:3]
        top3 = [
            {
                "class": CLASS_NAMES[int(index)],
                "confidence": round(float(predictions[int(index)]) * 100, 2),
            }
            for index in top3_indices
        ]

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "description": disease_info["description"],
            "treatment": disease_info["treatment"],
            "severity": disease_info["severity"],
            "top3": top3,
            "is_healthy": disease_info["severity"] == "None",
        }


predictor = PlantDiseasePredictor()
