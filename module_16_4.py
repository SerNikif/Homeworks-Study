from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users', response_model=List[User])
async def Get_Users() -> List[User]:
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def Post_User(
        username: Annotated[str, Path(description="Имя пользователя")],
        age: Annotated[int, Path(description="Возраст пользователя")]) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def Update_User(user_id: Annotated[int, Path(description="ID User")],
                      username: Annotated[str, Path(description="Username")],
                      age: Annotated[int, Path(description="Age User")]) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        user.username = username
        user.age = age
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}', response_model=User)
async def Delete_User(user_id: Annotated[int, Path(description="ID User")]) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        users.remove(user)
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")
