from fastapi import FastAPI

from config import db
from models import UserModel

app = FastAPI(
    title="Library Management System API",
    summary="Application uses FastAPI to add REST API to a MongoDB Collection",
    description="""
                Helps to manage library resources among its users
                
                ## Users
                
                Able to:
                
                * **Create users**
                * **Read users**
                * **Update users**
                * **Delete users**
                """
)

user_collection = db.get_collection("User")


@app.get("/")
def get_health_status():
    return {"Hello": "World"}


@app.post(
    "/users/",
    response_description="Add new User",
    response_model=UserModel,
    response_model_by_alias=False,
    status_code=201,
)
async def create_user(user: UserModel):
    """
    create_user route receives the new_user data as a JSON string in POST request
    We have to decode this JSON request body into a python dictionary
    before passing it to MongoDB Client

    :param user:
    :return:
    """
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user
