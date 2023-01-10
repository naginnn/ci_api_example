from dataclasses import asdict
from sanic import Blueprint, json
from sanic_ext import validate
from app1.shemas.clusters import Cluster
from app1.utils.clusters import get_all_clusters, create_cluster, get_one_cluster
from auth.utils.auth import protected

cluster_config = Blueprint("ClusterConfig", url_prefix="/ClustersConfiguration", version=1, version_prefix="/api/v")

@cluster_config.get('/Clusters')
@protected
async def get_clusters(request):
    clusters = await get_all_clusters()
    return json({'clusters': clusters})

@cluster_config.get('/Clusters/configurations/<cluster_id>')
@protected
async def get_cluster(request, cluster_id: str):
    cluster = await get_one_cluster(cluster_id)
    return json({"cluster": cluster})

@cluster_config.post('/Clusters/configurations/create')
@validate(query=Cluster)
@protected
async def create(request, query: Cluster):
    cluster_id = await create_cluster(asdict(query))
    return json({'cluster_id': str(cluster_id)})


# http://127.0.0.1:8000/api/v1/ClustersConfiguration
# http://127.0.0.1:8000/v1/ClustersConfiguration/cluster?name=dsads

