"""Tests unitaires pour le composant de nettoyage et de feature engineering."""

import pandas as pd
from src.processing.cleaner import DataCleaner


def test_simplify_processor() -> None:
    """Valide le regroupement des processeurs."""
    cleaner = DataCleaner()
    assert cleaner.simplify_processor("Intel Core i7-10875H") == "Intel Core i7"
    assert cleaner.simplify_processor("Apple M1 Pro") == "Apple Silicon"
    assert cleaner.simplify_processor("AMD Ryzen 5 5600U") == "AMD Ryzen 5"
    assert cleaner.simplify_processor("Intel Celeron N4020") == "Other"


def test_clean_dataframe_pipeline() -> None:
    """Valide l'élimination des doublons, prix aberrants et le calcul des ratios."""
    raw_records = [
        {"brand": "dell", "model": "XPS", "processor": "Intel Core i5", "ram_gb": 8, "storage_gb": 256, "storage_type": "SSD", "screen_size_inch": 13.3, "condition": "Très bon état", "price_eur": 350.0},
        # Doublon exact du premier
        {"brand": "dell", "model": "XPS", "processor": "Intel Core i5", "ram_gb": 8, "storage_gb": 256, "storage_type": "SSD", "screen_size_inch": 13.3, "condition": "Très bon état", "price_eur": 350.0},
        # Prix aberrant (< 50€)
        {"brand": "HP", "model": "EliteBook", "processor": "AMD Ryzen 5", "ram_gb": 16, "storage_gb": 512, "storage_type": "SSD", "screen_size_inch": 14.0, "condition": "Bon état", "price_eur": 10.0},
        # Cas Apple
        {"brand": "apple", "model": "MacBook Air", "processor": "Apple M1", "ram_gb": 16, "storage_gb": 512, "storage_type": "SSD", "screen_size_inch": 13.3, "condition": "Parfait état", "price_eur": 850.0},
    ]
    df_raw = pd.DataFrame(raw_records)
    cleaner = DataCleaner()
    df_clean = cleaner.clean_dataframe(df_raw)

    # Doit rester 2 lignes (doublon éliminé, prix aberrant éliminé)
    assert len(df_clean) == 2
    assert "Dell" in df_clean["brand"].values
    assert "Apple" in df_clean["brand"].values
    assert df_clean.loc[df_clean["brand"] == "Apple", "is_apple"].values[0] == 1
    assert df_clean.loc[df_clean["brand"] == "Dell", "condition_score"].values[0] == 3
    assert df_clean.loc[df_clean["brand"] == "Dell", "storage_per_ram_ratio"].values[0] == 32.0  # 256 / 8
