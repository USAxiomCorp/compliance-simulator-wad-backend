"""
Singleton holder for the FinancialComplianceSuperintelligence instance.
In-memory only — state lives for the lifetime of the Render worker process.
"""
from compliance_engine import FinancialComplianceSuperintelligence

_system_instance: FinancialComplianceSuperintelligence | None = None

def get_system() -> FinancialComplianceSuperintelligence:
    global _system_instance
    if _system_instance is None:
        _system_instance = FinancialComplianceSuperintelligence()
    return _system_instance
