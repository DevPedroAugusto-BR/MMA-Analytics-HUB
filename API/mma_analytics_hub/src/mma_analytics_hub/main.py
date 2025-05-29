from fastapi import FastAPI
from http import HTTPStatus

from mma_analytics_hub.schemas import (
    UserSchema,
    UserPublic,
    UserDB,
    FighterSchema,
    FighterList,
    FighterDB,
    FighterPublic,
    WeightClassSchema,
    WeightClassDB,
    FighterPublic,
)

app = FastAPI()

database = []

@app.get("/fighter", status_code=HTTPStatus.OK, response_model=FighterList)
def read_root():
    return {"message": "Olá Mundo!"}


@app.post("/create_user", status_code=HTTPStatus.CREATED, response_model=FighterList)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)  

    database.append(user_with_id)

    return user_with_id

@app.put("/update_user/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.put("/update_fighter/{fighter_id}", status_code=HTTPStatus.OK, response_model=FighterPublic)
def update_fighter(fighter_id: int, fighter: FighterSchema):
    ...