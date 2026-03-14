from fastapi import APIRouter, HTTPException, Query
from services.dashboard_service import (
    get_feature_table_data,
    get_clusters_data,
    get_cluster_samples_data,
)

router = APIRouter(tags=["dashboard"])


@router.get("/features/table")
async def get_feature_table():
    try:
        return get_feature_table_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clusters")
async def get_clusters():
    try:
        return get_clusters_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clusters/{cluster_id}/samples")
async def get_cluster_samples(cluster_id: int, limit: int = Query(15, ge=1, le=100)):
    try:
        return get_cluster_samples_data(cluster_id=cluster_id, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))