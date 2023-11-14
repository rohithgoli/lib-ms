from fastapi import FastAPI
from config import db_client

app = FastAPI()


#TODO: Debug the DB client connection
@app.get("/")
async def check_db_health():
    try:
        await db_client.admin.command('ping')
        print("Pinged current deployment. You successfully connected to MongoDB!")
        return {"Hello": "World"}
    except Exception as e:
        print(e)
        return {"Hello": "Check MongoDB"}
