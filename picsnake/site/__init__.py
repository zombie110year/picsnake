from .sm_ms import ISession as SmmsSession

__all__ = ("INTERGRATED_BEDS", "SmmsSession")

INTERGRATED_BEDS = {
    "sm.ms": SmmsSession,
}
