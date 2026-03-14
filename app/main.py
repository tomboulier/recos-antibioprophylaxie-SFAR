"""Point d'entrée FastAPI — Antibioprophylaxie SFAR."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import interventions_router, specialites_router
from app.config import _PROJECT_ROOT, Settings
from app.data.loader import load_rfe_data
from app.web.routes import router as web_router

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from app.data.models import RFEData

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Charge les données RFE en mémoire au démarrage du serveur."""
    rfe_data = load_rfe_data(settings.data_path)
    app.state.rfe_data = rfe_data
    app.state.settings = settings
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "API de consultation des recommandations d'antibioprophylaxie chirurgicale (RFE SFAR 2024)"
    ),
    version=settings.app_version,
    lifespan=lifespan,
)

_templates = Jinja2Templates(directory=str(_PROJECT_ROOT / "app" / "templates"))

app.mount("/static", StaticFiles(directory=str(_PROJECT_ROOT / "app" / "static")), name="static")
app.include_router(interventions_router)
app.include_router(specialites_router)
app.include_router(web_router)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> HTMLResponse:
    """Page 404 personnalisée : JSON pour les routes API, HTML sinon."""
    from fastapi.responses import JSONResponse

    if request.url.path.startswith("/api/"):
        detail = getattr(exc, "detail", "Ressource non trouvée.")
        return JSONResponse(status_code=404, content={"detail": detail})
    return HTMLResponse(
        content=_templates.get_template("404.html").render({"request": request}),
        status_code=404,
    )


def get_rfe_data() -> RFEData:
    """Accès aux données RFE chargées en mémoire."""
    return app.state.rfe_data


@app.get("/api/v1/health")
def health() -> dict:
    """Health check endpoint."""
    rfe: RFEData = app.state.rfe_data
    total_interventions = sum(len(s.interventions) for s in rfe.specialites)
    return {
        "status": "ok",
        "version": settings.app_version,
        "data_version": settings.data_version,
        "specialites": len(rfe.specialites),
        "interventions": total_interventions,
    }
