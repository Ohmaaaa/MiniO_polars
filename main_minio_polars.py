import subprocess
import os

def run_script(script_name):
    print(f"\n🚀 Exécution de : {script_name}")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"❌ Erreur dans {script_name} :\n{result.stderr}")
        exit(1)

def main():
    print("🔄 Démarrage complet du pipeline : Extract ➝ Transform ➝ Load")

    # Vérifier que le .env existe
    if not os.path.exists(".env"):
        print("❌ Fichier .env manquant. Création impossible.")
        return

    # Étape 1 : Extraction depuis MinIO
    run_script("extract_minio_polars.py")

    # Étape 2 : Transformation des données
    run_script("transform_minio_polars.py")

    # Étape 3 : Chargement dans SQLite
    run_script("load_minio_polars.py")

    print("\n✅ Pipeline ETL terminé avec succès. Données prêtes dans 'stocks.db'.")

if __name__ == "__main__":
    main()
