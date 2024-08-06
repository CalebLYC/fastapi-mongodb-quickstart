import motor.motor_asyncio

from config.enviro import env


#Déterminer l'environnement et chosir la base de données correspondnate
enviro = env('ENV')
if enviro == 'production':
    database_uri = env('DATABASE_URI_TEST')
else:
    database_uri = env('DATABASE_URI_PROD')

#Charger le client du SGBD MongoDB avec motor
client = motor.motor_asyncio.AsyncIOMotorClient(database_uri)
#Récupérer la base de donnees api_concours
db = client.api_concours