from fastapi import FastAPI, HTTPException, Path, Query,Depends
from typing import Optional, List, Dict, Annotated
from models import User,Post 
from database import  session_local
from schemas import Аuthor,PostCreate,UserCreate
from auth import get_current_user, router,get_password_hash,oauth2_scheme
import uvicorn
# Создание экземпляра FastAPI

app = FastAPI()



# Эндпоинт для получения всех постов
@app.get("/items")
async def items(post: PostCreate) -> PostCreate:
    return post

# Эндпоинт для добавления нового поста
@app.post("/items/add")
async def add_item(post: PostCreate) -> PostCreate:
    # Поиск автора поста по ID

    return post  # Возвращаем созданный пост


# Эндпоинт для добавления нового пользователя
@app.post("/user/add")
async def user_add(user: Annotated[UserCreate, Query(...)]):
    # Генерация нового ID для пользователя
    user.password= get_password_hash(user.password)
    async with session_local() as session:
        user = User(login=user.login, password=user.password)
        session.add(user)
        await session.commit()
    # Создание нового пользователя
    
    return ("Вы зарегистрировались в системе")  # Возвращаем созданного пользователя


# Эндпоинт для получения поста по ID
@app.get("/items/get")
async def items(id: Annotated[int, Query(..., title='Здесь указывается id поста', ge=1)]) -> PostCreate:
    # Поиск поста по ID
    raise HTTPException(status_code=404, detail="Input number: not more 3!!!")


# Эндпоинт для поиска поста по ID через query-параметр
@app.get("/search")
async def search(post_id: Annotated[
    Optional[int],
    Query(title="ID of post to search for", ge=1, le=50)
],token: str = Depends(get_current_user)) :

        return {'data': None}  # Если post_id не указан, возвращаем None

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
