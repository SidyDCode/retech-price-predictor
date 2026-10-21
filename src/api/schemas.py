"""Schémas Pydantic pour la validation des requêtes et réponses de l'API."""

from pydantic import BaseModel, Field


class LaptopPredictionRequest(BaseModel):
    """Données d'entrée obligatoires pour estimer un prix."""

    brand: str = Field(..., examples=["Dell"], description="Marque de l'ordinateur")
    processor: str = Field(..., examples=["Intel Core i5"], description="Modèle brut du processeur")
    ram_gb: int = Field(..., ge=2, le=128, examples=[16], description="Mémoire vive en Go")
    storage_gb: int = Field(..., ge=64, le=4096, examples=[512], description="Espace de stockage en Go")
    screen_size_inch: float = Field(..., ge=10.0, le=20.0, examples=[14.0], description="Diagonale d'écran en pouces")
    condition: str = Field(..., examples=["Très bon état"], description="État esthétique du PC")


class LaptopPredictionResponse(BaseModel):
    """Format de la réponse renvoyée par le modèle."""

    predicted_price_eur: float = Field(..., description="Prix estimé recommandé en euros")
    status: str = Field(default="success", description="Statut de l'inférence")
    model_version: str = Field(default="0.1.0", description="Version du modèle déployé")
