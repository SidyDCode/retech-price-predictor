"""Tests unitaires pour l'entraînement et l'inférence du modèle ML."""

import pandas as pd
from src.models.train import ModelTrainer


def test_model_training_and_inference(tmp_path) -> None:
    """Valide l'entraînement complet et la prédiction sur un cas neuf."""
    # Création d'un dataset minimal contrôlé
    records = []
    for i in range(40):
        records.append({
            "brand": "Dell" if i % 2 == 0 else "Apple",
            "processor_group": "Intel Core i5" if i % 2 == 0 else "Apple Silicon",
            "ram_gb": 8 if i % 2 == 0 else 16,
            "storage_gb": 256 if i % 2 == 0 else 512,
            "screen_size_inch": 14.0,
            "condition_score": 3,
            "storage_per_ram_ratio": 32.0,
            "price_eur": 300.0 if i % 2 == 0 else 750.0,
        })
    df_dummy = pd.DataFrame(records)
    parquet_path = tmp_path / "dummy_clean.parquet"
    df_dummy.to_parquet(parquet_path, index=False)

    model_dest = tmp_path / "test_model.joblib"
    trainer = ModelTrainer(data_path=parquet_path, output_model_path=model_dest)
    summary = trainer.train_and_evaluate()

    assert model_dest.exists()
    assert summary["best_model_name"] != ""
    assert "mae" in summary["best_metrics"]

    # Test d'inférence avec le pipeline sauvegardé
    import joblib
    saved_pipeline = joblib.load(model_dest)
    sample_input = pd.DataFrame([{
        "ram_gb": 16,
        "storage_gb": 512,
        "screen_size_inch": 14.0,
        "condition_score": 3,
        "storage_per_ram_ratio": 32.0,
        "brand": "Dell",
        "processor_group": "Intel Core i5",
    }])
    predicted_price = float(saved_pipeline.predict(sample_input)[0])
    assert predicted_price > 0.0
