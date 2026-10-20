"""Tests unitaires pour le module d'analyse exploratoire (EDA)."""

import pandas as pd
from src.processing.eda import ExploratoryAnalysis


def test_exploratory_analysis_workflow(tmp_path) -> None:
    """Valide les calculs d'agrégation et la génération des fichiers images de manière isolée."""
    # Création d'un fichier Parquet temporaire autonome pour le test
    dummy_data = pd.DataFrame({
        "brand": ["Dell", "Dell", "Apple", "HP"],
        "price_eur": [300.0, 400.0, 900.0, 250.0],
    })
    dummy_parquet = tmp_path / "test_data.parquet"
    dummy_data.to_parquet(dummy_parquet, index=False)

    # Exécution avec les chemins temporaires
    eda = ExploratoryAnalysis(data_path=dummy_parquet, output_dir=tmp_path)

    stats = eda.compute_summary_statistics()
    assert not stats.empty
    assert "prix_median" in stats.columns
    assert "prix_moyen" in stats.columns

    p1 = eda.plot_price_distribution()
    p2 = eda.plot_price_by_brand()

    assert p1.exists()
    assert p2.exists()
    assert p1.stat().st_size > 0
    assert p2.stat().st_size > 0
