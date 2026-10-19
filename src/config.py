"""Module de configuration globale du projet.

Gère la localisation dynamique des répertoires et les paramètres
d'environnement pour garantir la portabilité du code.
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Paramètres et chemins structurels du projet."""

    # Racine du projet : deux niveaux au-dessus de src/config.py
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent

    # Répertoires de données
    DATA_DIR: Path = ROOT_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

    # Répertoire des artefacts de modèles entraînés
    MODELS_DIR: Path = ROOT_DIR / "models"

    # Environnement
    APP_NAME: str = "retech-price-predictor"
    APP_VERSION: str = "0.1.0"


# Instance unique (Singleton) importable partout dans le projet
settings = Settings()
