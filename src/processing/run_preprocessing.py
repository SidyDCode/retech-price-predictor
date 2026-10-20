"""Script exécutable pour transformer les données SQL brutes en données prêtes pour le ML."""

import pandas as pd
from sqlalchemy.orm import Session

from src.config import settings
from src.ingestion.database import engine
from src.ingestion.models_sql import LaptopListingDB
from src.processing.cleaner import DataCleaner


def export_cleaned_data() -> None:
    """Charge depuis SQL, applique le nettoyage et sauvegarde en Parquet."""
    print("-> Chargement des données brutes depuis SQL...")
    with Session(engine) as session:
        query = session.query(LaptopListingDB).statement
        df_raw = pd.read_sql(query, session.bind)

    if df_raw.empty:
        print("Attention : la base SQL est vide. Pensez à exécuter IngestionPipeline d'abord.")
        return

    print(f"-> {len(df_raw)} annonces chargées. Début du nettoyage...")
    cleaner = DataCleaner()
    df_cleaned = cleaner.clean_dataframe(df_raw)

    output_path = settings.PROCESSED_DATA_DIR / "laptops_cleaned.parquet"
    df_cleaned.to_parquet(output_path, index=False)
    print(f"-> Nettoyage terminé avec succès : {len(df_cleaned)} lignes exportées vers {output_path}")


if __name__ == "__main__":
    export_cleaned_data()
