"""Pipeline d'ingestion orchestrant l'extraction et le chargement en base SQL."""

from typing import List
from sqlalchemy.orm import Session

from src.ingestion.database import engine, Base, SessionLocal
from src.ingestion.scraper import LaptopScraper
from src.ingestion.models_sql import LaptopListingDB
from src.ingestion.schema import RawLaptopListing


class IngestionPipeline:
    """Orchestrateur du flux de données d'ingestion (ETL)."""

    def __init__(self, session: Session = None) -> None:
        self.session = session or SessionLocal()
        self.scraper = LaptopScraper()

    def create_tables(self) -> None:
        """Génère les tables dans la base si elles n'existent pas encore."""
        Base.metadata.create_all(bind=engine)

    def load_listings(self, listings: List[RawLaptopListing]) -> int:
        """Insère une liste d'annonces typées en base SQL."""
        db_records = [
            LaptopListingDB(
                brand=item.brand,
                model=item.model,
                processor=item.processor,
                ram_gb=item.ram_gb,
                storage_gb=item.storage_gb,
                storage_type=item.storage_type,
                screen_size_inch=item.screen_size_inch,
                condition=item.condition,
                price_eur=item.price_eur,
                source_url=item.source_url,
            )
            for item in listings
        ]

        self.session.add_all(db_records)
        self.session.commit()
        return len(db_records)

    def run_seed_pipeline(self, sample_size: int = 50) -> int:
        """Exécute un cycle complet avec le jeu de données de référence."""
        self.create_tables()
        listings = self.scraper.generate_seed_data(sample_size=sample_size)
        inserted_count = self.load_listings(listings)
        return inserted_count
