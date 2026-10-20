"""Gestion de la connexion à la base de données relationnelle via SQLAlchemy."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import settings

# Si une variable DATABASE_URL existe (ex: PostgreSQL), on la prend,
# sinon on utilise SQLite local dans le dossier data/
DEFAULT_SQLITE_PATH = settings.DATA_DIR / "retech.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")

# Configuration de l'Engine (connect_args requis uniquement pour SQLite multithread)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# Fabrique de sessions pour exécuter les transactions SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour la déclaration des modèles de tables
Base = declarative_base()


def get_db():
    """Générateur de session sécurisé avec fermeture automatique."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
