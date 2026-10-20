"""Schéma de validation des données brutes d'ordinateurs portables."""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class RawLaptopListing:
    """Structure typée d'une annonce d'ordinateur reconditionné."""

    brand: str
    model: str
    processor: str
    ram_gb: int
    storage_gb: int
    storage_type: str
    screen_size_inch: float
    condition: str
    price_eur: float
    source_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'instance en dictionnaire natif."""
        return asdict(self)
