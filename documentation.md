# 📦 Projet de Pipeline de Données avec MinIO, Polars, SQLite et Jenkins

## 🔧 Objectif du projet

Ce projet a pour but de démontrer une chaîne de traitement de données complète, depuis le stockage de fichiers bruts jusqu'à leur transformation et leur intégration dans une base de données relationnelle. Le tout est orchestré via une CI/CD automatisée.

---

## 🗂️ Étapes du pipeline

### 1. Stockage des données avec MinIO

- Un **bucket MinIO** a été créé pour héberger les fichiers de données (CSV, JSON, etc.).
- MinIO est une alternative S3-compatible utilisée comme solution de stockage objet locale.

### 2. Chargement et traitement des données avec Polars

- Les fichiers ont été récupérés depuis le bucket MinIO.
- Nous avons utilisé la librairie **Polars** (rapide et efficace en Rust/Python) pour charger les données.
- Les transformations incluent :
  - Nettoyage des colonnes
  - Conversion de types
  - Filtres et enrichissements
  - Agrégations selon les besoins métiers

### 3. Ingestion dans une base SQLite

- Une fois les données transformées, elles sont **insérées dans une base de données SQLite**.
- Ce choix léger permet des tests rapides et une portabilité maximale.

---

## ⚙️ Orchestration avec Jenkins

- Le processus complet est orchestré via un **pipeline Jenkins**.
- Jenkins automatise :
  - Le chargement des données
  - La transformation
  - L'insertion en base

> 💡 **Alternative** : Nous avons également envisagé une orchestration basée sur le **workflow Git (GitHub Actions ou GitLab CI)** pour une intégration directe dans le cycle de développement.

---

## 🚀 Déclenchement automatique

- Le pipeline est déclenché automatiquement **à chaque `git push`**.
- Cela permet une intégration continue des modifications de code, avec un traitement des données toujours à jour.

---

## ✅ Tests et vérifications

- Des **tests de pipeline** ont été mis en place pour garantir le bon fonctionnement de chaque étape :
  - Disponibilité du bucket MinIO
  - Bon chargement des données avec Polars
  - Exactitude des transformations
  - Intégrité des données en base SQLite
- Les tests sont intégrés au pipeline Jenkins et s'exécutent à chaque lancement.

---

## 📌 Résumé

| Étape                     | Technologie utilisée |
|--------------------------|----------------------|
| Stockage objet           | MinIO                |
| Traitement des données   | Polars               |
| Base de données cible    | SQLite               |
| Orchestration            | Jenkins / Git        |
| Tests automatisés        | Intégrés dans Jenkins|

---

## 🔄 Perspectives d'évolution

- Passage vers une base PostgreSQL ou BigQuery pour la production
- Migration vers des orchestrateurs comme **Apache Airflow** ou **Dagster**
- Intégration de validation de données avec **Great Expectations**

