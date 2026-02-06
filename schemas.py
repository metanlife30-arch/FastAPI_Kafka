from pydantic import BaseModel
from typing import  Annotated
from pydantic import BaseModel, Field


class Аuthor(BaseModel):
    id: int  # Уникальный идентификатор пользователя
    name: str  # Имя пользователя
    age: int  # Возраст пользователя



# Модель данных для создания нового поста
class PostCreate(BaseModel):
    title: str  # Заголовок поста
    body: str  # Текст поста
    author_id: int  # ID автора поста


# Модель данных для создания нового пользователя
class UserCreate(BaseModel):
    # Используем Annotated для добавления метаданных и валидации
    # Имя пользователя (от 2 до 20 символов), Имя пользователя (от 2 до 20 символов)
    login: Annotated[str, Field(..., title="login to log in to the system", min_length=2, max_length=20)]
    # Возраст пользователя (от 5 до 120 лет)
    password: Annotated[str, Field(..., title="password login to log in to the system", min_length=5)]