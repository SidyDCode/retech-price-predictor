"""Pipeline d'entraînement et de sélection du meilleur modèle ML."""

from pathlib import Path
from typing import Tuple, Dict, Any
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import settings
from src.models.evaluate import evaluate_predictions


class ModelTrainer:
    """Entraîne, compare et exporte les modèles de prédiction de prix."""

    NUMERICAL_FEATURES = ["ram_gb", "storage_gb", "screen_size_inch", "condition_score", "storage_per_ram_ratio"]
    CATEGORICAL_FEATURES = ["brand", "processor_group"]
    TARGET_COLUMN = "price_eur"

    def __init__(self, data_path: Path = None, output_model_path: Path = None) -> None:
        self.data_path = data_path or (settings.PROCESSED_DATA_DIR / "laptops_cleaned.parquet")
        self.output_model_path = output_model_path or (settings.ROOT_DIR / "models" / "best_model.joblib")
        self.output_model_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Charge le dataset Parquet et sépare features et cible."""
        df = pd.read_parquet(self.data_path)
        X = df[self.NUMERICAL_FEATURES + self.CATEGORICAL_FEATURES]
        y = df[self.TARGET_COLUMN]
        return X, y

    def build_preprocessor(self) -> ColumnTransformer:
        """Crée le transformateur Scikit-Learn pour les types mixtes."""
        num_transformer = StandardScaler()
        cat_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", num_transformer, self.NUMERICAL_FEATURES),
                ("cat", cat_transformer, self.CATEGORICAL_FEATURES),
            ]
        )
        return preprocessor

    def train_and_evaluate(self) -> Dict[str, Any]:
        """Exécute l'entraînement comparatif et enregistre le meilleur modèle."""
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        preprocessor = self.build_preprocessor()

        candidates = {
            "Baseline (Dummy Mean)": DummyRegressor(strategy="mean"),
            "Ridge Regression": Ridge(alpha=1.0),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        }

        results: Dict[str, Dict[str, float]] = {}
        fitted_pipelines: Dict[str, Pipeline] = {}

        for name, regressor in candidates.items():
            pipe = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", regressor)])
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_test)
            metrics = evaluate_predictions(y_test.values, preds)
            results[name] = metrics
            fitted_pipelines[name] = pipe

        # Sélection basée sur le plus haut score R2
        best_model_name = max(results, key=lambda k: results[k]["r2"])
        best_pipe = fitted_pipelines[best_model_name]

        joblib.dump(best_pipe, self.output_model_path)

        return {
            "results": results,
            "best_model_name": best_model_name,
            "best_metrics": results[best_model_name],
            "model_path": self.output_model_path,
        }


if __name__ == "__main__":
    trainer = ModelTrainer()
    summary = trainer.train_and_evaluate()
    print("=== Résultat des modèles comparés ===")
    for model_name, metrics in summary["results"].items():
        print(f"- {model_name} -> MAE: {metrics['mae']}€ | RMSE: {metrics['rmse']}€ | R2: {metrics['r2']}")
    print(f"\n-> Meilleur modèle : {summary['best_model_name']}")
    print(f"-> Artefact sauvegardé dans : {summary['model_path']}")
