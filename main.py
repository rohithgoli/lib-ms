from fastapi import FastAPI, Response, HTTPException
from bson import ObjectId
from pymongo import ReturnDocument

from config import db
from models import UserModel, UserCollection, UpdateUserModel

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


@app.get(
    "/users/{user_id}",
    response_description="Get a single user",
    response_model=UserModel,
    response_model_by_alias=False
)
async def fetch_user_by_id(user_id: str):
    if (desired_user := await user_collection.find_one(
        {"_id": ObjectId(user_id)}
    )) is not None:
        return desired_user
    raise HTTPException(status_code=404, detail=f"User {user_id} is not found")


@app.get(
    "/users",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False
)
async def list_users():
    """
    List all the users data in the database
    :return:
    """
    return UserCollection(users=await user_collection.find().to_list(None))


@app.put(
    "/users/{user_id}",
    response_description="Update a user",
    response_model=UserModel,
    response_model_by_alias=False
)
async def update_user(user_id: str, user: UpdateUserModel):
    user = {
        key: value for key, value in user.model_dump(by_alias=True).items() if value is not None
    }

    if len(user) >= 1:
        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if (current_user_document := await user_collection.find_one({"_id": ObjectId(user_id)})) is not None:
       return current_user_document

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.delete(
    "/users/{user_id}",
    response_description="Delete a user"
)
async def delete_student(user_id: str):
    delete_result = await user_collection.delete_one(
        {"_id": ObjectId(user_id)}
    )

    if delete_result.deleted_count == 1:
        return Response(status_code=204)

    raise HTTPException(status_code=204, detail=f"User {user_id} not found")
