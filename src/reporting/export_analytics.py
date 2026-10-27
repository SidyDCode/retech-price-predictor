"""Module d'exportation des données analytiques pour le reporting Power BI."""

from pathlib import Path
import joblib
import pandas as pd

from src.config import settings


class AnalyticsExporter:
    """Génère un jeu de données enrichi pour le tableau de bord décisionnel."""

    def __init__(self, data_path: Path = None, model_path: Path = None, output_path: Path = None) -> None:
        self.data_path = data_path or (settings.PROCESSED_DATA_DIR / "laptops_cleaned.parquet")
        self.model_path = model_path or (settings.ROOT_DIR / "models" / "best_model.joblib")
        self.output_path = output_path or (settings.PROCESSED_DATA_DIR / "analytics_powerbi.csv")

    def run_export(self) -> Path:
        """Charge les données, génère les prédictions et exporte le fichier CSV."""
        df = pd.read_parquet(self.data_path)
        model = joblib.load(self.model_path)

        # Inférence sur l'ensemble du jeu de données
        features = ["ram_gb", "storage_gb", "screen_size_inch", "condition_score", "storage_per_ram_ratio", "brand", "processor_group"]
        df["predicted_price_eur"] = model.predict(df[features]).round(2)

        # Calcul des écarts pour l'analyse financière solidaire
        df["price_diff_eur"] = (df["price_eur"] - df["predicted_price_eur"]).round(2)
        df["price_diff_pct"] = ((df["price_diff_eur"] / df["price_eur"]) * 100).round(1)

        # Export au format CSV standard UTF-8 avec séparateur point-virgule (adapté à Power BI France)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, sep=";", index=False, encoding="utf-8-sig")
        return self.output_path


if __name__ == "__main__":
    exporter = AnalyticsExporter()
    out = exporter.run_export()
    print(f"-> Données analytiques exportées avec succès : {out}")
