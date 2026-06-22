from fastapi import APIRouter
from app.api.endpoints import axioms, assess, pathways, metrics, health

router = APIRouter()
router.include_router(axioms.router,   prefix="/axioms",   tags=["Axioms"])
router.include_router(assess.router,   prefix="/assess",   tags=["Assessment"])
router.include_router(pathways.router, prefix="/pathways", tags=["Pathways"])
router.include_router(metrics.router,  prefix="/metrics",  tags=["Metrics"])
router.include_router(health.router,   prefix="/health",   tags=["Health"])
