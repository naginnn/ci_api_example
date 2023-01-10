import decimal
import json
import datetime

from app1.models.clusters import clusters_table
from app1.shemas.clusters import Cluster
from settings.database import database
from asyncpg.pgproto.pgproto import UUID


def alchemy_encoder(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def model_to_dict(model):
    d = json.dumps([dict(r) for r in model], default=alchemy_encoder)
    return json.loads(d)


async def get_all_clusters():
    query = clusters_table.select()
    async with database.connect() as conn:
        res = await conn.execute(query)
        return model_to_dict(res)


async def get_one_cluster(cluster_id):
    query = clusters_table.select().where(clusters_table.c.id == cluster_id)
    async with database.connect() as conn:
        res = await conn.execute(query)
        return model_to_dict(res)


async def create_cluster(cluster: Cluster):
    query = (
        clusters_table.insert().values(**cluster)
    )
    async with database.begin() as conn:
        cluster_id = await conn.execute(query)
        return cluster_id.inserted_primary_key[0]