"""FastAPI application for PlantDiseaseDetector."""

from __future__ import annotations

import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.model import CLASS_NAMES
from src.predictor import predictor

MODEL_PATH = Path("models/plant_disease_model.keras")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PlantDiseaseDetector",
    description="CNN-based classifier for tomato, potato, and bell pepper leaf diseases.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event() -> None:
    """Load the trained model at startup when it exists."""
    if MODEL_PATH.exists():
        predictor.load()
        logger.info("Loaded model from %s", MODEL_PATH)
    else:
        logger.warning(
            "No trained model found at %s. Train first with: python -m src.model data/PlantVillage",
            MODEL_PATH,
        )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> JSONResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload must be an image file.")

    if predictor.model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Train the model before predicting.")

    try:
        image_bytes = await file.read()
        result = predictor.predict(image_bytes)
        return JSONResponse(content=result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc


@app.get("/health")
async def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "model_loaded": predictor.model is not None,
        "model_path": str(MODEL_PATH),
    }


@app.get("/classes")
async def classes() -> dict[str, list[str] | int]:
    return {"classes": CLASS_NAMES, "total": len(CLASS_NAMES)}


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
