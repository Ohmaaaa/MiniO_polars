# 🚀 MinIO + Polars + SQLite Pipeline

## Description
Ce projet lit un fichier CSV stocké sur MinIO, applique des transformations avec Polars, puis charge les résultats dans une base SQLite. Idéal pour des besoins BI / Data Science.

## Structure
- `transform_minio_polars.py` : extraction et transformation
- `load_minio_polars.py` : chargement en base SQLite
- `.env` : configuration MinIO

## Installation

```bash
pip install -r requirements.txt
