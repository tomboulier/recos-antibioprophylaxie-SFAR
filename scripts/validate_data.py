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
    """Charge et valide data/rfe.json avec les modèles Pydantic.

    Raises
    ------
    FileNotFoundError
        Si le fichier data/rfe.json est introuvable.
    ValueError
        Si des erreurs de cohérence sont détectées.
    """
    if not DATA_PATH.exists():
        msg = f"{DATA_PATH} introuvable."
        raise FileNotFoundError(msg)

    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data = RFEData.model_validate(raw)

    # Statistiques
    nb_specialites = len(data.specialites)
    nb_interventions = sum(len(s.interventions) for s in data.specialites)
    nb_avec_protocole = sum(
        1 for s in data.specialites for i in s.interventions if i.protocole is not None
    )
    nb_sans_protocole = nb_interventions - nb_avec_protocole

    print(f"Validation OK — {data.version}")
    print(f"  Spécialités   : {nb_specialites}")
    print(f"  Interventions : {nb_interventions}")
    print(f"    avec ATB    : {nb_avec_protocole}")
    print(f"    sans ATB    : {nb_sans_protocole}")

    # Vérifications de cohérence
    errors: list[str] = []
    ids_seen: set[str] = set()
    for spec in data.specialites:
        for interv in spec.interventions:
            # IDs uniques
            if interv.id in ids_seen:
                errors.append(f"ID dupliqué : {interv.id}")
            ids_seen.add(interv.id)

            # Cohérence protocole / alternative_allergie
            if interv.protocole is None and interv.alternative_allergie is not None:
                errors.append(
                    f"{interv.id} : pas de protocole mais alternative_allergie renseignée"
                )

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
        msg = f"{len(errors)} erreur(s) de cohérence détectée(s)"
        raise ValueError(msg)

    print("  Cohérence     : OK")
    return data


if __name__ == "__main__":
    try:
        validate()
    except (FileNotFoundError, ValueError) as e:
        print(f"ERREUR : {e}")
        sys.exit(1)
