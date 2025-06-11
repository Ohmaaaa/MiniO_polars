#!/usr/bin/env python

import os
import sys
import logging

import polars as pl
from dotenv import load_dotenv

# ──────────────
# CONFIG LOGGING
# ──────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def get_storage_options():
    """Construit les options de connexion MinIO à partir du .env"""
    try:
        return {
            "key": os.environ["MINIO_ACCESS_KEY"],
            "secret": os.environ["MINIO_SECRET_KEY"],
            "client_kwargs": {
                "endpoint_url": os.environ["MINIO_ENDPOINT"],
            },
        }
    except KeyError as e:
        logger.error(f"Variable d’environnement manquante : {e}")
        raise


def main():
    load_dotenv()  # charge les variables d’environnement depuis .env

    file_path = "s3://yahoo/stock_details_5_years.csv"

    try:
        storage_options = get_storage_options()

        logger.info("📥 Début de l'extraction depuis MinIO : %s", file_path)

        df = pl.read_csv(
            file_path,
            storage_options=storage_options,
            dtypes={"Stock Splits": pl.Float64},
            infer_schema_length=0
        )

        logger.info("✅ Extraction réussie. Aperçu des données :")
        print(df.head())

    except Exception as e:
        logger.exception(f"❌ Erreur pendant l'extraction : {e}")
        sys.exit(1)  # exit code ≠ 0 → échec pour Jenkins


if __name__ == "__main__":
    main()
