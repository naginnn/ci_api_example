import uvicorn
from sanic.config import Config

from app1.routers.clusters import cluster_config
from auth.routers.login import login
from auth.utils.auth import protected
from settings.database import database
from sanic import Sanic, text
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

_sessionmaker = sessionmaker(database, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")

app = Sanic("ClusterDiscovery")

app.config.API_BASEPATH = "/api"
app.config.API_VERSION = "1.0.0"
app.config.FALLBACK_ERROR_FORMAT = "json"
app.blueprint(cluster_config)
app.config.SECRET = "hui_sraniy"
app.blueprint(login)
# app.config.OAS_UI_SWAGGER = False

@app.before_server_start
async def setup_db(app):
    app.ctx.db = await database.connect()

@app.before_server_stop
async def close_db(app):
    app.ctx.db = await database.dispose()

# @app.middleware("request")
# async def inject_session(request):
#     request.ctx.session = _sessionmaker()
#     request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)
#
#
# @app.middleware("response")
# async def close_session(request, response):
#     if hasattr(request.ctx, "session_ctx_token"):
#         _base_model_session_ctx.reset(request.ctx.session_ctx_token)
#         await request.ctx.session.close()

@app.get("/secret")
@protected
async def secret(request):
    return text("To go fast, you must be fast.")

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8001)
    uvicorn.run(app)