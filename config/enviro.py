import os
from dotenv import load_dotenv

#Charger toutes les variables d'environnement
load_dotenv()

#Fonction pour récupérer une variable d'environment défini dans le .env
def env(variable: str):
    return os.getenv(variable)