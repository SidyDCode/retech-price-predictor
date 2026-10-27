"""Module d'analyse exploratoire des données (EDA)."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import settings


class ExploratoryAnalysis:
    """Générateur d'indicateurs statistiques et de visualisations de données."""

    def __init__(self, data_path: Path = None, output_dir: Path = None) -> None:
        self.data_path = data_path or (settings.PROCESSED_DATA_DIR / "laptops_cleaned.parquet")
        self.output_dir = output_dir or (settings.ROOT_DIR / "reports" / "figures")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.df = pd.read_parquet(self.data_path)

        # Style visuel sobre et professionnel
        sns.set_theme(style="whitegrid")

    def compute_summary_statistics(self) -> pd.DataFrame:
        """Calcule les métriques clés de prix par marque."""
        stats = (
            self.df.groupby("brand")["price_eur"]
            .agg(nombre_annonces="count", prix_moyen="mean", prix_median="median", ecart_type="std")
            .round(2)
            .sort_values(by="prix_median", ascending=False)
        )
        return stats

    def plot_price_distribution(self) -> Path:
        """Génère l'histogramme de la distribution des prix avec courbe de densité."""
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(self.df["price_eur"], kde=True, color="#2b5c8f", ax=ax)
        ax.set_title("Distribution des prix de revente estimés (€)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Prix (€)")
        ax.set_ylabel("Effectif")

        save_path = self.output_dir / "price_distribution.png"
        fig.tight_layout()
        fig.savefig(save_path, dpi=300)
        plt.close(fig)
        return save_path

    def plot_price_by_brand(self) -> Path:
        """Génère un graphique comparatif des prix moyens par marque avec barres d'écart-type."""
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(
            data=self.df,
            x="brand",
            y="price_eur",
            hue="brand",
            palette="Set2",
            legend=False,
            errorbar="sd",
            ax=ax,
        )
        ax.set_title("Prix moyen par marque (avec écart-type)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Marque")
        ax.set_ylabel("Prix moyen (€)")

        save_path = self.output_dir / "price_by_brand.png"
        fig.tight_layout()
        fig.savefig(save_path, dpi=300)
        plt.close(fig)
        return save_path

    def plot_features_correlation(self) -> Path:
        """Génère la matrice de corrélation thermique des variables numériques."""
        numeric_cols = self.df.select_dtypes(include=["number"]).columns
        corr = self.df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr,
            annot=True,
            cmap="Blues",
            fmt=".2f",
            linewidths=0.5,
            cbar=True,
            ax=ax,
        )
        ax.set_title("Matrice de corrélation des variables numériques", fontsize=13, fontweight="bold")

        save_path = self.output_dir / "features_correlation.png"
        fig.tight_layout()
        fig.savefig(save_path, dpi=300)
        plt.close(fig)
        return save_path

    def run_full_analysis(self) -> None:
        """Exécute l'analyse statistique et génère l'ensemble des graphiques."""
        print("=== Indicateurs statistiques par marque ===")
        print(self.compute_summary_statistics())

        p1 = self.plot_price_distribution()
        p2 = self.plot_price_by_brand()
        p3 = self.plot_features_correlation()

        print(f"\n-> Graphiques exportés dans : {self.output_dir}")
        print(f"   1. {p1.name}")
        print(f"   2. {p2.name}")
        print(f"   3. {p3.name}")


if __name__ == "__main__":
    eda = ExploratoryAnalysis()
    eda.run_full_analysis()