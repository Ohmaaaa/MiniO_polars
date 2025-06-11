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


def transform(df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Effectue les transformations et agrégations sur les données."""
    logger.info("🧪 Début des transformations")

    parsed = pl.col("Date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S%z")

    df = df.with_columns(
        [
            parsed.alias("Parsed_Date"),
            (pl.col("Close") - pl.col("Open")).alias("Daily_Change"),
            ((pl.col("Close") - pl.col("Open")) / pl.col("Open") * 100).alias("Daily_Percent_Change"),
            pl.col("Volume").cast(pl.Int64),
            parsed.dt.year().alias("Year"),
            parsed.dt.month().alias("Month"),
            parsed.dt.strftime("%Y-%m").alias("Year_Month")
        ]
    ).filter(pl.col("Parsed_Date") >= pl.datetime(2020, 1, 1, time_unit="us", time_zone="UTC"))

    monthly_avg = (
        df.group_by(["Company", "Year_Month"])
        .agg([
            pl.col("Close").mean().alias("Monthly_Avg_Close"),
            pl.col("Volume").mean().alias("Monthly_Avg_Volume")
        ])
        .sort(["Company", "Year_Month"])
    )

    return df, monthly_avg


def main():
    load_dotenv()
    file_path = "s3://yahoo/stock_details_5_years.csv"

    try:
        logger.info("📥 Lecture du CSV depuis MinIO")
        storage_options = get_storage_options()

        df = pl.read_csv(
            file_path,
            storage_options=storage_options,
            dtypes={"Stock Splits": pl.Float64},
            infer_schema_length=0
        )

        df_transformed, monthly_avg = transform(df)

        df_transformed.write_parquet("df_transformed.parquet")
        monthly_avg.write_parquet("monthly_avg.parquet")

        logger.info("✅ Fichiers Parquet sauvegardés avec succès")

    except Exception as e:
        logger.exception("❌ Échec de la transformation : %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
