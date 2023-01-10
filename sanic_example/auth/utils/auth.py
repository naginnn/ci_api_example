from functools import wraps
import jwt
from sanic import text
import hashlib
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import and_

from app1.utils.clusters import model_to_dict
from auth.models import users
from auth.models.users import users_table, tokens_table
from auth.shemas.users import UserCreate, UserAuth
from settings.database import database


def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # is_authenticated = check_token(request)
            user = await get_user_by_token(request.token)
            if user:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_token_by_user(user: UserAuth):
    """ Возвращает токен пользователя """
    query = users_table.select().where(users_table.c.first_name == user.first_name)
    async with database.connect() as conn:
        res = await conn.execute(query)
    hashed_password = model_to_dict(res)[0].get('hashed_password')
    if validate_password(user.password, hashed_password):
        query = tokens_table.select()
        async with database.connect() as conn:
            res = await conn.execute(query)
        res = model_to_dict(res)
    return res[0].get('token')

#
#
async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    async with database.connect() as conn:
        res = await conn.execute(query)
        return res.fetchone()
#
#
async def create_user_token(user_id: int):
    """ Создает токен для пользователя с указанным user_id """
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(weeks=2),
                user_id=user_id,
                token=jwt.encode({}, str(user_id)))
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )
    async with database.begin() as conn:
        token = await conn.execute(query)

    return token.fetchone()


async def create_user(query: dict):
    user = UserCreate(**query)
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        role=user.role, first_name=user.first_name, hashed_password=f"{salt}${hashed_password}"
    )
    async with database.begin() as conn:
        user_id = await conn.execute(query)

    user_id = user_id.inserted_primary_key[0]
    token, expires = await create_user_token(user_id)
    token_dict = {"token": token, "expires": expires}
    res = {**user.__dict__, "id": str(user_id), "is_active": True, "token": str(token)}
    return res


