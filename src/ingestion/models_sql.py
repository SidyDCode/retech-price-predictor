"""Déclaration des tables SQL du projet."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from src.ingestion.database import Base


def get_utc_now() -> datetime:
    """Renvoie la date et heure courante en UTC (fuseau explicite)."""
    return datetime.now(timezone.utc)


class LaptopListingDB(Base):
    """Table de stockage des annonces brutes d'ordinateurs portables."""

    __tablename__ = "laptop_listings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand = Column(String(50), nullable=False, index=True)
    model = Column(String(100), nullable=False)
    processor = Column(String(100), nullable=False)
    ram_gb = Column(Integer, nullable=False)
    storage_gb = Column(Integer, nullable=False)
    storage_type = Column(String(20), nullable=False)
    screen_size_inch = Column(Float, nullable=False)
    condition = Column(String(50), nullable=False)
    price_eur = Column(Float, nullable=False)
    source_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self) -> str:
        return f"<LaptopListingDB(id={self.id}, brand='{self.brand}', price={self.price_eur}€)>"
