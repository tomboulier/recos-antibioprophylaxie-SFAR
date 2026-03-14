"""Routers de l'API REST /api/v1/."""

from __future__ import annotations

from app.api.interventions import router as interventions_router
from app.api.specialites import router as specialites_router

__all__ = ["interventions_router", "specialites_router"]
