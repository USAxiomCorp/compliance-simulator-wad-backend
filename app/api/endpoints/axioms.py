from fastapi import APIRouter, HTTPException
from app.core.engine import get_system

router = APIRouter()

@router.get("/")
def list_axioms():
    """Return all 8 registered FCA axioms."""
    system = get_system()
    return {
        axiom_id: {
            "name": ax.name,
            "statement": ax.statement,
            "certainty": ax.certainty,
            "nuclear_charge": ax.nuclear_charge,
            "mathematical_form": ax.mathematical_form,
            "regulatory_basis": ax.regulatory_basis,
            "enforcement_agency": ax.enforcement_agency,
            "penalty_for_violation": ax.penalty_for_violation,
        }
        for axiom_id, ax in system.axiom_registry.items()
    }

@router.get("/{axiom_id}")
def get_axiom(axiom_id: str):
    """Return a single axiom by ID (F1–F8)."""
    system = get_system()
    ax = system.axiom_registry.get(axiom_id.upper())
    if not ax:
        raise HTTPException(status_code=404, detail=f"Axiom '{axiom_id}' not found. Valid IDs: F1–F8.")
    return {
        "name": ax.name,
        "statement": ax.statement,
        "certainty": ax.certainty,
        "nuclear_charge": ax.nuclear_charge,
        "mathematical_form": ax.mathematical_form,
        "regulatory_basis": ax.regulatory_basis,
        "enforcement_agency": ax.enforcement_agency,
        "penalty_for_violation": ax.penalty_for_violation,
    }
