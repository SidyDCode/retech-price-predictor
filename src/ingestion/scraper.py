"""Module d'ingestion et d'extraction de données web (POO)."""

import random
from typing import List
from bs4 import BeautifulSoup
import requests

from src.ingestion.schema import RawLaptopListing


class LaptopScraper:
    """Extracteur de listings de PC portables reconditionnés."""

    def __init__(self, base_url: str = "https://example-refurbished.local", timeout: int = 10) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def fetch_page_content(self, url: str) -> str:
        """Récupère le HTML brut d'une page avec gestion des exceptions réseau."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            # En cas d'échec ou d'absence de réseau, on renvoie une chaîne vide
            return ""

    def parse_html_listings(self, html_content: str) -> List[RawLaptopListing]:
        """Parse le contenu HTML pour extraire les cartes produits."""
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        listings: List[RawLaptopListing] = []

        # Recherche des conteneurs de produits
        cards = soup.select(".product-card")
        for card in cards:
            try:
                brand = card.select_one(".brand").get_text(strip=True) if card.select_one(".brand") else "Unknown"
                model = card.select_one(".model").get_text(strip=True) if card.select_one(".model") else "Generic"
                price_str = card.select_one(".price").get_text(strip=True).replace("€", "").replace(",", ".").strip()
                
                listings.append(
                    RawLaptopListing(
                        brand=brand,
                        model=model,
                        processor="Intel Core i5",
                        ram_gb=8,
                        storage_gb=256,
                        storage_type="SSD",
                        screen_size_inch=14.0,
                        condition="Très bon état",
                        price_eur=float(price_str),
                    )
                )
            except (ValueError, AttributeError):
                continue

        return listings

    def generate_seed_data(self, sample_size: int = 50) -> List[RawLaptopListing]:
        """Génère un jeu de données de référence réaliste pour alimenter la base."""
        brands = ["Dell", "Lenovo", "HP", "Apple", "Asus"]
        processors = ["Intel Core i5", "Intel Core i7", "AMD Ryzen 5", "AMD Ryzen 7", "Apple M1"]
        conditions = ["État correct", "Bon état", "Très bon état", "Parfait état"]

        seed: List[RawLaptopListing] = []
        random.seed(42)  # Déterminisme pour tests reproductibles

        for i in range(sample_size):
            brand = random.choice(brands)
            ram = random.choice([8, 16, 32])
            storage = random.choice([256, 512, 1024])
            screen = random.choice([13.3, 14.0, 15.6])
            condition = random.choice(conditions)
            proc = "Apple M1" if brand == "Apple" else random.choice(processors[:4])

            # Règle de prix empirique de départ
            base_price = 150.0 + (ram * 12.0) + (storage * 0.25)
            if brand == "Apple":
                base_price *= 1.4
            if condition == "Parfait état":
                base_price *= 1.2

            seed.append(
                RawLaptopListing(
                    brand=brand,
                    model=f"{brand} Pro {i+1}",
                    processor=proc,
                    ram_gb=ram,
                    storage_gb=storage,
                    storage_type="SSD",
                    screen_size_inch=screen,
                    condition=condition,
                    price_eur=round(base_price, 2),
                    source_url=f"https://solidarite-retech.org/listing/{i+1}",
                )
            )

        return seed
