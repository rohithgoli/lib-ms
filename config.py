import certifi
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient

secrets = dotenv_values(".env")

db_client = AsyncIOMotorClient(
    secrets['DB_CONNECTION_STRING'],
    tlsCAFile=certifi.where()
)
db = db_client.get_database("libMS")
