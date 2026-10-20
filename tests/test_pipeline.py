"""Tests d'intégration pour le pipeline de persistance SQL."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.ingestion.database import Base
from src.ingestion.models_sql import LaptopListingDB
from src.ingestion.pipeline import IngestionPipeline


def test_ingestion_pipeline_in_memory() -> None:
    """Valide l'exécution complète de l'ingestion sur une base SQL en mémoire."""
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()

    # Exécution du pipeline
    pipeline = IngestionPipeline(session=session)
    inserted = pipeline.run_seed_pipeline(sample_size=20)

    # Vérifications
    assert inserted == 20
    rows = session.query(LaptopListingDB).all()
    assert len(rows) == 20
    assert rows[0].brand in ["Dell", "Lenovo", "HP", "Apple", "Asus"]
    assert rows[0].price_eur > 0

    session.close()
