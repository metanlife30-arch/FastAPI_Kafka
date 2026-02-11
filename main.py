from fastapi import FastAPI, HTTPException, Path, status, Query,Depends 
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Annotated
from sqlalchemy import select
from fastapi.responses import JSONResponse
from models import User,Post,Аuthor 
from database import  session_local, engine
from schemas import АuthorCreate,PostCreate,UserCreate,Post_delete,Аuthor_delete
from auth import get_current_user, router,get_password_hash,oauth2_scheme
import uvicorn
# Создание экземпляра FastAPI

app = FastAPI()

# Эндпоинт для получения всех постов
@app.get("/post/all",summary="All post",tags=["Posts"])
async def items(token: str = Depends(get_current_user)):
    async with session_local() as session:
        result = await session.execute(select(Post))
        posts = result.scalars().all()
        return  posts

# Эндпоинт для добавления нового поста
@app.post("/post/add",summary="Add post",tags=["Posts"])
async def add_item(post: PostCreate,token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        post = Post(title=post.title, body=post.body, author_id=post.author_id)
        session.add(post)
        await session.commit()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')    
        return ("Данные успешно добавлены")  # Возвращаем созданный пост

# Эндпоинт для удаление поста
@app.delete("/post/delete",summary="Delete post",tags=["Posts"])
async def add_item(post: Annotated[Post_delete,Query(...,title="delete", description="id post")],token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        post = await session.get(Post,post.id)
        await session.delete(post)
        await session.commit()
    return (f"Пост успешно удалён {post.id}")  # Возвращаем созданный пост

# Эндпоинт для добавления нового пользователя
@app.post("/user/add",tags=["User"])
async def user_add(user: Annotated[UserCreate, Query(...)]):
    # Генерация нового ID для пользователя
    user.password= get_password_hash(user.password)
    async with session_local() as session:
        user = User(login=user.login, password=user.password)
        session.add(user)
        await session.commit()
    # Создание нового пользователя
    
    return ("Вы зарегистрировались в системе")  # Возвращаем созданного пользователя


# Эндпоинт для добавления нового автора
@app.post("/author/add",summary="Add author",tags=["Author"])
async def add_item(author: АuthorCreate,token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        post = Аuthor(name=author.name, age=author.age)
        session.add(post)
        await session.commit()
    return (f"Автор успешно добавлен {author}")  # Возвращаем созданный пост

# Эндпоинт для удаление автора
@app.delete("/author/delete",summary="Delete author",tags=["Author"])
async def add_item(author: Annotated[Аuthor_delete,Query(...,title="delete", description="id post")],token: str = Depends(get_current_user)):
    # Поиск автора поста по ID
    async with session_local() as session:
        author = await session.get(Аuthor,author.id)
        await session.delete(author)
        await session.commit()
    return (f"Автор успешно удалён c id {author.id}")  # Возвращаем созданный пост



app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
