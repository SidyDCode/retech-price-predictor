"""Tests unitaires pour le composant d'ingestion."""

from src.ingestion.scraper import LaptopScraper
from src.ingestion.schema import RawLaptopListing


def test_seed_data_generation() -> None:
    """Vérifie la génération des données d'ingestion et leur typage."""
    scraper = LaptopScraper()
    items = scraper.generate_seed_data(sample_size=10)

    assert len(items) == 10
    first = items[0]

    assert isinstance(first, RawLaptopListing)
    assert first.brand in ["Dell", "Lenovo", "HP", "Apple", "Asus"]
    assert first.ram_gb in [8, 16, 32]
    assert first.price_eur > 0.0


def test_parse_html_listings() -> None:
    """Vérifie l'extraction HTML sur un fragment de test contrôlé."""
    html_mock = """
    <div class="product-card">
        <span class="brand">Lenovo</span>
        <span class="model">ThinkPad T480</span>
        <span class="price">280,00 €</span>
    </div>
    """
    scraper = LaptopScraper()
    listings = scraper.parse_html_listings(html_mock)

    assert len(listings) == 1
    assert listings[0].brand == "Lenovo"
    assert listings[0].model == "ThinkPad T480"
    assert listings[0].price_eur == 280.0
