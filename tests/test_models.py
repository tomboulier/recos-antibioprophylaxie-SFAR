"""Tests pour les modèles Pydantic et la validation des données."""

import json
from pathlib import Path

import pytest

from app.data.models import (
    AlternativeAllergie,
    Intervention,
    Protocole,
    RFEData,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "rfe.json"


# ── Fixtures ──────────────────────────────────────────────────────────


@pytest.fixture()
def rfe_data() -> RFEData:
    """Charge et valide data/rfe.json."""
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return RFEData.model_validate(raw)


# ── Tests unitaires modèles ───────────────────────────────────────────


class TestProtocole:
    def test_creation_complete(self):
        p = Protocole(
            molecule="Céfazoline",
            posologie="2g IVL",
            reinjection="1g toutes les 4h",
            duree="Durée de l'intervention",
        )
        assert p.molecule == "Céfazoline"
        assert p.reinjection == "1g toutes les 4h"

    def test_reinjection_optionnelle(self):
        p = Protocole(
            molecule="Gentamicine",
            posologie="6-7 mg/kg",
            duree="Dose unique",
        )
        assert p.reinjection is None


class TestAlternativeAllergie:
    def test_creation(self):
        alt = AlternativeAllergie(
            molecule="Clindamycine",
            posologie="900mg IVL",
        )
        assert alt.molecule == "Clindamycine"
        assert alt.reinjection is None


class TestIntervention:
    def test_intervention_avec_abp(self):
        interv = Intervention(
            id="test-abp",
            nom="Test avec ABP",
            specialite="Test",
            protocole=Protocole(
                molecule="Céfazoline",
                posologie="2g IVL",
                duree="Durée de l'intervention",
            ),
            force_recommandation="Avis d'experts",
            source_page=73,
            source_tableau="Tableau test",
        )
        assert not interv.pas_d_abp
        assert interv.protocole is not None

    def test_intervention_sans_abp(self):
        interv = Intervention(
            id="test-pas-abp",
            nom="Test sans ABP",
            specialite="Test",
            pas_d_abp=True,
            force_recommandation="GRADE 2",
            source_page=74,
            source_tableau="Tableau test",
        )
        assert interv.pas_d_abp
        assert interv.protocole is None
        assert interv.alternative_allergie is None


# ── Tests sur data/rfe.json ───────────────────────────────────────────


class TestRFEDataStructure:
    def test_json_valide(self, rfe_data: RFEData):
        """Le JSON se charge et passe la validation Pydantic."""
        assert rfe_data.version.startswith("RFE SFAR 2024")

    def test_au_moins_une_specialite(self, rfe_data: RFEData):
        assert len(rfe_data.specialites) >= 1

    def test_specialites_attendues(self, rfe_data: RFEData):
        noms = {s.nom for s in rfe_data.specialites}
        assert "Chirurgie orthopédique programmée" in noms
        assert "Traumatologie" in noms

    def test_interventions_non_vides(self, rfe_data: RFEData):
        for spec in rfe_data.specialites:
            assert len(spec.interventions) > 0, f"{spec.nom} est vide"


class TestRFEDataCoherence:
    def test_ids_uniques(self, rfe_data: RFEData):
        ids = [i.id for s in rfe_data.specialites for i in s.interventions]
        assert len(ids) == len(set(ids)), "IDs en doublon"

    def test_specialite_coherente(self, rfe_data: RFEData):
        """Le champ specialite de chaque intervention correspond au nom de sa spécialité."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                assert interv.specialite == spec.nom, (
                    f"{interv.id}: specialite='{interv.specialite}' != '{spec.nom}'"
                )

    def test_coherence_pas_d_abp_protocole(self, rfe_data: RFEData):
        """Si pas_d_abp=True → protocole=None ; sinon protocole renseigné."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                if interv.pas_d_abp:
                    assert interv.protocole is None, (
                        f"{interv.id}: pas_d_abp mais protocole renseigné"
                    )
                else:
                    assert interv.protocole is not None, (
                        f"{interv.id}: ABP indiquée mais protocole manquant"
                    )

    def test_force_recommandation_valeurs(self, rfe_data: RFEData):
        valeurs_valides = {"Avis d'experts", "GRADE 1", "GRADE 2"}
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                assert interv.force_recommandation in valeurs_valides, (
                    f"{interv.id}: force_recommandation '{interv.force_recommandation}' inattendue"
                )

    def test_source_page_positive(self, rfe_data: RFEData):
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                assert interv.source_page > 0, f"{interv.id}: source_page={interv.source_page}"


class TestRFEDataContenu:
    def test_nombre_interventions_ortho(self, rfe_data: RFEData):
        ortho = next(
            s for s in rfe_data.specialites if s.id == "chirurgie-orthopedique-programmee"
        )
        # 4 sous-sections : MI(9) + Épaule(10) + Main(5) + Rachis(6) = 30
        assert len(ortho.interventions) == 30

    def test_nombre_interventions_trauma(self, rfe_data: RFEData):
        trauma = next(s for s in rfe_data.specialites if s.id == "traumatologie")
        # Fractures fermées(3) + ouvertes(2) + plaies(4) + main(8) = 17
        assert len(trauma.interventions) == 17

    def test_prothese_hanche_a_protocole(self, rfe_data: RFEData):
        """La PTH est un cas classique avec ABP céfazoline."""
        ortho = next(
            s for s in rfe_data.specialites if s.id == "chirurgie-orthopedique-programmee"
        )
        pth = next(
            i
            for i in ortho.interventions
            if "hanche" in i.nom.lower() and "prothèse" in i.nom.lower()
        )
        assert not pth.pas_d_abp
        assert pth.protocole is not None
        assert pth.protocole.molecule == "Céfazoline"
        assert pth.alternative_allergie is not None
        assert len(pth.alternative_allergie) >= 1

    def test_arthroscopie_sans_materiel_pas_abp(self, rfe_data: RFEData):
        """L'arthroscopie diagnostique sans matériel n'a pas d'ABP."""
        ortho = next(
            s for s in rfe_data.specialites if s.id == "chirurgie-orthopedique-programmee"
        )
        arthro = next(
            i
            for i in ortho.interventions
            if "arthroscopie" in i.nom.lower()
            and "sans" in i.nom.lower()
            and "membre inférieur" not in i.nom.lower()
        )
        assert arthro.pas_d_abp

    def test_gustilo_2_3_amoxicilline(self, rfe_data: RFEData):
        """Les fractures ouvertes Gustilo 2-3 utilisent Amoxicilline/Clavulanate."""
        trauma = next(s for s in rfe_data.specialites if s.id == "traumatologie")
        gustilo23 = next(i for i in trauma.interventions if "gustilo 2" in i.nom.lower())
        assert gustilo23.protocole is not None
        assert "Amoxicilline" in gustilo23.protocole.molecule
