pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
    }

    stages {
        stage('Setup') {
            steps {
                echo '🔧 Création de l’environnement virtuel et installation des dépendances...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Tests') {
            steps {
                echo '🧪 Exécution des tests...'
                bat '''
                    call venv\\Scripts\\activate
                    python -m unittest discover -s tests
                '''
            }
        }

        stage('Extract') {
            steps {
                echo '📥 Extraction des données...'
                bat '''
                    call venv\\Scripts\\activate
                    python extract_minio_polars.py
                '''
            }
        }

        stage('Transform') {
            steps {
                echo '🔄 Transformation des données...'
                bat '''
                    call venv\\Scripts\\activate
                    python transform_minio_polars.py
                '''
            }
        }

        stage('Load') {
            steps {
                echo '📤 Chargement des données...'
                bat '''
                    call venv\\Scripts\\activate
                    python load_minio_polars.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline ETL terminée avec succès !'
        }
        failure {
            echo '❌ Échec de la pipeline. Vérifie les logs.'
        }
    }
}
