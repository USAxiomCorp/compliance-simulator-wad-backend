from fastapi import APIRouter
from app.core.engine import get_system

router = APIRouter()

@router.get("/")
def get_session_metrics():
    """Return all R³ refinement cycle snapshots for this session."""
    system = get_system()
    return {
        "total_cycles": len(system.session_metrics),
        "intelligence_level": system.r3_processor.intelligence_level,
        "cycles": [
            {
                "cycle": m.cycle,
                "pathway_strength": m.pathway_strength,
                "emergence_metric": m.emergence_metric,
                "total_confidence": m.total_confidence,
                "axioms_coverage": m.axioms_coverage,
                "safety_gates_passed": m.safety_gates_passed,
                "regulatory_approval_status": m.regulatory_approval_status,
                "intelligence_level": m.intelligence_level,
                "timestamp": m.timestamp,
            }
            for m in system.session_metrics
        ],
    }
