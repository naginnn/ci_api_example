from dataclasses import asdict
import jwt
from sanic import Blueprint, text, json, response
import secrets
from sanic_ext import validate
from auth.shemas.users import UserCreate, UserAuth
from auth.utils.auth import create_user, get_token_by_user

# login = Blueprint("login", url_prefix="/login")
login = Blueprint("login")


@login.post("/login")
@validate(query=UserAuth)
async def do_login(request, query: UserAuth):
    request.app.config.SECRET = secrets.token_urlsafe(16)
    print(asdict(query))
    token = await get_token_by_user(query)
    # token = jwt.encode({}, request.app.config.SECRET)
    return text(token)



@login.post("/sign-up")
@validate(query=UserCreate)
async def sign_up(request, query: UserCreate):
    user = await create_user(asdict(query))
    return json(user)