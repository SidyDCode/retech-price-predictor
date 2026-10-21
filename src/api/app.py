"""Point d'entrée du serveur API FastAPI."""

from contextlib import asynccontextmanager
from typing import Dict, Any
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.config import settings
from src.processing.cleaner import DataCleaner
from src.api.schemas import LaptopPredictionRequest, LaptopPredictionResponse

# Variable globale pour stocker le pipeline en mémoire RAM
model_pipeline = None


def load_model_from_disk():
    """Charge l'artefact de modèle sauvegardé."""
    global model_pipeline
    model_path = settings.ROOT_DIR / "models" / "best_model.joblib"
    if not model_path.exists():
        raise RuntimeError(f"Le fichier modèle est introuvable : {model_path}")
    model_pipeline = joblib.load(model_path)
    return model_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cycle de vie de l'application : charge le modèle au démarrage."""
    load_model_from_disk()
    yield
    global model_pipeline
    model_pipeline = None


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API solidaire d'estimation de prix de PC reconditionnés",
    lifespan=lifespan,
)


@app.get("/health", tags=["Monitoring"])
def health_check() -> Dict[str, str]:
    """Vérifie que l'API est en ligne et opérationnelle."""
    return {"status": "ok", "app_name": settings.APP_NAME, "version": settings.APP_VERSION}


@app.post("/predict", response_model=LaptopPredictionResponse, tags=["Inférence"])
def predict_price(payload: LaptopPredictionRequest) -> Dict[str, Any]:
    """Reçoit les spécifications d'un PC et renvoie le prix estimé."""
    global model_pipeline
    if model_pipeline is None:
        try:
            model_pipeline = load_model_from_disk()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Modèle non disponible : {str(e)}")

    # 1. Feature Engineering
    cleaner = DataCleaner()
    proc_group = cleaner.simplify_processor(payload.processor)
    condition_score = cleaner.CONDITION_MAPPING.get(payload.condition, 2)
    ratio = round(payload.storage_gb / payload.ram_gb, 2)

    # 2. DataFrame adapté pour Scikit-Learn
    input_data = pd.DataFrame([{
        "ram_gb": payload.ram_gb,
        "storage_gb": payload.storage_gb,
        "screen_size_inch": payload.screen_size_inch,
        "condition_score": condition_score,
        "storage_per_ram_ratio": ratio,
        "brand": payload.brand.strip().capitalize(),
        "processor_group": proc_group,
    }])

    # 3. Inférence
    try:
        raw_pred = model_pipeline.predict(input_data)[0]
        final_price = round(float(raw_pred), 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'inférence : {str(e)}")

    return {
        "predicted_price_eur": final_price,
        "status": "success",
        "model_version": settings.APP_VERSION,
    }
