# Retech Price Predictor 💻

> Pipeline de données de bout en bout et API de Machine Learning pour l'estimation du prix de revente d'ordinateurs portables reconditionnés à destination d'associations solidaires.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange?logo=scikitlearn)
![Pytest](https://img.shields.io/badge/Tests-12%20passed-brightgreen?logo=pytest)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🎯 Contexte Métier
Les associations de réinsertion et structures solidaires collectent régulièrement des parcs informatiques d'occasion sans disposer d'une visibilité claire sur leur valeur marchande résiduelle. Ce projet vise à :
1. **Automatiser la collecte** et l'ingestion d'annonces de matériel reconditionné.
2. **Nettoyer et fiabiliser** les spécifications techniques (processeur, mémoire vive, stockage, état).
3. **Entraîner un modèle de Machine Learning supervisé** capable de proposer un prix de revente équitable.
4. **Exposer le modèle via une API REST** haute performance pour intégration dans des outils de gestion ou des applications web.

---

## 🏗️ Architecture du Projet

```text
retech-price-predictor/
├── data/
│   ├── raw/                  # Données brutes issues de l'ingestion
│   └── processed/            # Parquet nettoyé & exports CSV analytiques
├── models/
│   └── best_model.joblib     # Pipeline complet (preprocessing + modèle)
├── reports/
│   └── figures/              # Graphiques d'EDA (distributions, boxplots)
├── src/
│   ├── api/                  # Application FastAPI, endpoints & schémas Pydantic
│   ├── database/             # Modèles SQLAlchemy & gestion des sessions
│   ├── ingestion/            # Scraper orienté objet & pipeline ETL
│   ├── models/               # Entraînement, comparaison de modèles & métriques
│   ├── processing/           # Nettoyage, feature engineering & EDA
│   ├── reporting/            # Exports de données décisionnelles (Power BI)
│   └── config.py             # Configuration centralisée via Pydantic Settings
├── tests/                    # 12 tests automatisés (Scraping, SQL, Cleaning, ML, API)
├── requirements.txt
└── README.md