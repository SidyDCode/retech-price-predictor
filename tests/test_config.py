"""Tests unitaires pour la configuration globale."""

from pathlib import Path
from src.config import settings


def test_settings_paths_exist() -> None:
    """Vérifie que les répertoires stratégiques du projet existent."""
    assert settings.ROOT_DIR.exists()
    assert settings.ROOT_DIR.is_dir()
    assert settings.RAW_DATA_DIR.exists()
    assert settings.RAW_DATA_DIR.is_dir()
    assert settings.PROCESSED_DATA_DIR.exists()
    assert settings.PROCESSED_DATA_DIR.is_dir()


def test_project_metadata() -> None:
    """Vérifie le nom et la version de base du projet."""
    assert settings.APP_NAME == "retech-price-predictor"
    assert settings.APP_VERSION == "0.1.0"
