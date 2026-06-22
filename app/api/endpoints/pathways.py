from fastapi import APIRouter, HTTPException
from app.core.engine import get_system

router = APIRouter()

@router.get("/")
def list_pathways():
    """List all compliance pathways in the in-memory ledger."""
    system = get_system()
    return {
        "count": len(system.pathway_ledger),
        "pathways": [
            {
                "pathway_id": p.pathway_id,
                "query": p.query,
                "pathway_strength": p.pathway_strength,
                "emergence_metric": p.emergence_metric,
                "total_confidence": p.total_confidence,
                "axioms_used": sorted(p.axioms_used),
                "regulatory_approval_status": p.regulatory_approval_status,
                "conforms": p.conforms(),
                "step_count": len(p.steps),
            }
            for p in system.pathway_ledger
        ],
    }

@router.get("/{pathway_id}")
def get_pathway(pathway_id: str):
    """Return a single pathway with full step detail."""
    system = get_system()
    pathway = next((p for p in system.pathway_ledger if p.pathway_id == pathway_id), None)
    if not pathway:
        raise HTTPException(status_code=404, detail=f"Pathway '{pathway_id}' not found.")

    return {
        "pathway_id": pathway.pathway_id,
        "query": pathway.query,
        "pathway_strength": pathway.pathway_strength,
        "emergence_metric": pathway.emergence_metric,
        "total_confidence": pathway.total_confidence,
        "axioms_used": sorted(pathway.axioms_used),
        "regulatory_approval_status": pathway.regulatory_approval_status,
        "conforms": pathway.conforms(),
        "conclusion": pathway.conclusion,
        "steps": [
            {
                "step_id": s.step_id,
                "step_type": s.step_type.value,
                "transformation": s.transformation,
                "grounding_axioms": s.grounding_axioms,
                "confidence": s.confidence,
                "safety_validated": s.safety_validated,
                "regulatory_citations": s.regulatory_citations,
                "ontological_trace": s.ontological_trace,
                "mdm_components_used": s.mdm_components_used,
            }
            for s in pathway.steps
        ],
    }
