#!/usr/bin/env python3
"""Validation Pydantic du fichier data/rfe.json.

Usage :
    uv run python scripts/validate_data.py
"""

import json
import sys
from pathlib import Path

from app.data.models import RFEData

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "rfe.json"


def validate() -> RFEData:
    """Charge et valide data/rfe.json avec les modèles Pydantic."""
    if not DATA_PATH.exists():
        print(f"ERREUR : {DATA_PATH} introuvable.")
        sys.exit(1)

    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data = RFEData.model_validate(raw)

    # Statistiques
    nb_specialites = len(data.specialites)
    nb_interventions = sum(len(s.interventions) for s in data.specialites)
    nb_avec_abp = sum(1 for s in data.specialites for i in s.interventions if not i.pas_d_abp)
    nb_sans_abp = nb_interventions - nb_avec_abp

    print(f"Validation OK — {data.version}")
    print(f"  Spécialités   : {nb_specialites}")
    print(f"  Interventions : {nb_interventions}")
    print(f"    avec ABP    : {nb_avec_abp}")
    print(f"    sans ABP    : {nb_sans_abp}")

    # Vérifications de cohérence
    errors: list[str] = []
    ids_seen: set[str] = set()
    for spec in data.specialites:
        for interv in spec.interventions:
            # IDs uniques
            if interv.id in ids_seen:
                errors.append(f"ID dupliqué : {interv.id}")
            ids_seen.add(interv.id)

            # Cohérence pas_d_abp / protocole
            if interv.pas_d_abp and interv.protocole is not None:
                errors.append(f"{interv.id} : pas_d_abp=True mais protocole renseigné")
            if not interv.pas_d_abp and interv.protocole is None:
                errors.append(f"{interv.id} : pas_d_abp=False mais protocole manquant")

            # Cohérence specialite
            if interv.specialite != spec.nom:
                errors.append(
                    f"{interv.id} : specialite '{interv.specialite}' "
                    f"!= nom de la spécialité '{spec.nom}'"
                )

    if errors:
        print(f"\n  {len(errors)} erreur(s) de cohérence :")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)

    print("  Cohérence     : OK")
    return data


if __name__ == "__main__":
    validate()
