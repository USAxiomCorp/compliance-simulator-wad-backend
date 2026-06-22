from fastapi import APIRouter
from app.core.engine import get_system

router = APIRouter()

@router.get("/")
def health():
    system = get_system()
    return {
        "status": "operational",
        "axioms_loaded": len(system.axiom_registry),
        "pathways_in_ledger": len(system.pathway_ledger),
        "session_cycles": len(system.session_metrics),
        "intelligence_level": system.r3_processor.intelligence_level,
    }
