"""Module de nettoyage et de Feature Engineering pour les PC portables."""

from typing import List, Dict
import pandas as pd
import numpy as np


class DataCleaner:
    """Transformateur de données brutes vers un jeu de données prêt pour le ML."""

    CONDITION_MAPPING: Dict[str, int] = {
        "État correct": 1,
        "Bon état": 2,
        "Très bon état": 3,
        "Parfait état": 4,
    }

    @staticmethod
    def simplify_processor(processor: str) -> str:
        """Catégorise les processeurs pour réduire la cardinalité."""
        proc = str(processor).lower()
        if "apple" in proc or "m1" in proc or "m2" in proc:
            return "Apple Silicon"
        if "i7" in proc:
            return "Intel Core i7"
        if "i5" in proc:
            return "Intel Core i5"
        if "ryzen 7" in proc:
            return "AMD Ryzen 7"
        if "ryzen 5" in proc:
            return "AMD Ryzen 5"
        return "Other"

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique l'ensemble du pipeline de nettoyage sur un DataFrame."""
        if df.empty:
            return pd.DataFrame()

        data = df.copy()

        # 1. Dédoublonnage
        data = data.drop_duplicates(subset=["brand", "model", "processor", "ram_gb", "storage_gb", "price_eur"])

        # 2. Filtrage des valeurs aberrantes de prix
        data = data[(data["price_eur"] >= 50.0) & (data["price_eur"] <= 4000.0)]

        # 3. Standardisation des catégories textuelles
        data["brand"] = data["brand"].astype(str).str.strip().str.capitalize()
        data["processor_group"] = data["processor"].apply(self.simplify_processor)

        # 4. Encodage ordinal de l'état d'usure
        data["condition_score"] = data["condition"].map(self.CONDITION_MAPPING).fillna(2).astype(int)

        # 5. Feature Engineering métier
        data["storage_per_ram_ratio"] = (data["storage_gb"] / data["ram_gb"]).round(2)
        data["is_apple"] = (data["brand"] == "Apple").astype(int)

        # 6. Typage propre des colonnes numériques
        data["ram_gb"] = data["ram_gb"].astype(int)
        data["storage_gb"] = data["storage_gb"].astype(int)
        data["screen_size_inch"] = data["screen_size_inch"].astype(float)
        data["price_eur"] = data["price_eur"].astype(float)

        return data.reset_index(drop=True)
