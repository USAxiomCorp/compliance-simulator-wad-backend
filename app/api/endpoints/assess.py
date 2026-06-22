import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.core.engine import get_system
from compliance_engine import FinancialCustomer, FinancialTransaction

router = APIRouter()


class CustomerInput(BaseModel):
    customer_id: str
    full_name: str
    date_of_birth: str
    ssn_hash: str
    address: str
    annual_income: float = Field(gt=0)
    employment_status: str
    credit_score: int = Field(ge=300, le=850)
    kyc_verified: bool = False
    aml_risk_tier: str = "LOW"
    protected_class_flags: Dict[str, Any] = {}


class TransactionInput(BaseModel):
    transaction_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    transaction_type: str = "CREDIT_APPLICATION"
    counterparty_id: str = "BANK-HQ"
    channel: str = "DIGITAL"
    anomaly_score: float = Field(default=0.0, ge=0.0, le=1.0)
    sar_required: bool = False
    fraud_flag: bool = False


class CreditApplicationRequest(BaseModel):
    customer: CustomerInput
    transaction: TransactionInput


@router.post("/credit")
def assess_credit_application(request: CreditApplicationRequest):
    """
    Primary discovery workflow — assess a credit application through the full
    L1→L2→L3→L4 compliance loop with R³ refinement (7 cycles).
    """
    system = get_system()

    try:
        customer = FinancialCustomer(
            customer_id=request.customer.customer_id,
            full_name=request.customer.full_name,
            date_of_birth=request.customer.date_of_birth,
            ssn_hash=request.customer.ssn_hash,
            address=request.customer.address,
            annual_income=request.customer.annual_income,
            employment_status=request.customer.employment_status,
            credit_score=request.customer.credit_score,
            kyc_verified=request.customer.kyc_verified,
            aml_risk_tier=request.customer.aml_risk_tier,
            protected_class_flags=request.customer.protected_class_flags,
        )

        transaction = FinancialTransaction(
            transaction_id=request.transaction.transaction_id,
            customer_id=request.customer.customer_id,
            amount=request.transaction.amount,
            currency=request.transaction.currency,
            transaction_type=request.transaction.transaction_type,
            timestamp=time.time(),
            counterparty_id=request.transaction.counterparty_id,
            channel=request.transaction.channel,
            anomaly_score=request.transaction.anomaly_score,
            sar_required=request.transaction.sar_required,
            fraud_flag=request.transaction.fraud_flag,
        )

        result = system.assess_credit_application(customer, transaction)
        decision = result["decision"]
        pathway = result["pathway"]
        metrics_history = result["metrics_history"]

        return {
            "decision": {
                "decision_id": decision.decision_id,
                "customer_id": decision.customer_id,
                "requested_amount": decision.requested_amount,
                "approved": decision.approved,
                "approved_amount": decision.approved_amount,
                "interest_rate": decision.interest_rate,
                "decision_rationale": decision.decision_rationale,
                "explainability_score": decision.explainability_score,
                "disparate_impact_ratio": decision.disparate_impact_ratio,
                "regulatory_citations": decision.regulatory_citations,
                "model_version": decision.model_version,
            },
            "pathway_summary": {
                "pathway_id": pathway.pathway_id,
                "pathway_strength": pathway.pathway_strength,
                "emergence_metric": pathway.emergence_metric,
                "total_confidence": pathway.total_confidence,
                "axioms_used": sorted(pathway.axioms_used),
                "regulatory_approval_status": pathway.regulatory_approval_status,
                "conforms": pathway.conforms(),
                "step_count": len(pathway.steps),
            },
            "r3_summary": {
                "cycles_completed": len(metrics_history),
                "intelligence_level": result["intelligence_level"],
                "final_gates_passed": metrics_history[-1].safety_gates_passed if metrics_history else 0,
                "axioms_coverage": metrics_history[-1].axioms_coverage if metrics_history else 0.0,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance engine error: {str(e)}")
