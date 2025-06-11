#!/usr/bin/env python

import os
import sys
import logging
import sqlite3

import polars as pl

# ──────────────
# CONFIG LOGGING
# ──────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def load_parquet_to_sqlite():
    """Charge les fichiers Parquet transformés dans une base SQLite"""
    try:
        logger.info("📦 Lecture des fichiers Parquet")
        df_transformed = pl.read_parquet("df_transformed.parquet")
        monthly_avg = pl.read_parquet("monthly_avg.parquet")

        # Conversion en DataFrame Pandas
        logger.info("🔄 Conversion Polars → Pandas")
        df_transformed_pd = df_transformed.to_pandas()
        monthly_avg_pd = monthly_avg.to_pandas()

        # Connexion SQLite
        db_path = "stocks.db"
        conn = sqlite3.connect(db_path)
        logger.info(f"🔌 Connexion à la base SQLite : {db_path}")

        # Insertion dans les tables
        df_transformed_pd.to_sql("daily_data", conn, if_exists="replace", index=False)
        monthly_avg_pd.to_sql("monthly_avg", conn, if_exists="replace", index=False)

        conn.close()
        logger.info("✅ Données chargées dans SQLite avec succès")

    except FileNotFoundError as e:
        logger.error(f"❌ Fichier introuvable : {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"❌ Erreur lors du chargement des données dans SQLite : {e}")
        sys.exit(1)


if __name__ == "__main__":
    load_parquet_to_sqlite()
