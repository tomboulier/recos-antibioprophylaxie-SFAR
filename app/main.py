"""Point d'entrée FastAPI — Antibioprophylaxie SFAR."""

from fastapi import FastAPI

app = FastAPI(
    title="Antibioprophylaxie SFAR",
    description=(
        "API de consultation des recommandations d'antibioprophylaxie chirurgicale (RFE SFAR 2024)"
    ),
    version="0.1.0",
)


@app.get("/api/v1/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0", "data_version": "RFE SFAR 2024"}
