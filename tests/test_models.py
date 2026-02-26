"""Tests pour les modèles Pydantic et la validation des données."""

import json
from pathlib import Path

import pytest

from app.data.models import (
    ForceRecommandation,
    Intervention,
    Molecule,
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


class TestMolecule:
    def test_valeurs_enum(self):
        assert Molecule.CEFAZOLINE == "Céfazoline"
        assert Molecule.CLINDAMYCINE == "Clindamycine"
        assert Molecule.VANCOMYCINE == "Vancomycine"
        assert Molecule.TEICOPLANINE == "Teicoplanine"
        assert Molecule.AMOXICILLINE_CLAVULANATE == "Amoxicilline/Clavulanate"

    def test_enum_depuis_string(self):
        assert Molecule("Céfazoline") == Molecule.CEFAZOLINE

    def test_associations(self):
        assert Molecule.CLINDAMYCINE_GENTAMICINE == "Clindamycine + Gentamicine"
        assert Molecule.CEFAZOLINE_GENTAMICINE == "Céfazoline + Gentamicine"


class TestProtocole:
    def test_creation_complete(self):
        p = Protocole(
            molecule="Céfazoline",
            dose_initiale="2g IVL",
            reinjection="1g toutes les 4h",
            duree="Durée de l'intervention",
        )
        assert p.molecule == Molecule.CEFAZOLINE
        assert p.reinjection == "1g toutes les 4h"

    def test_reinjection_et_duree_optionnelles(self):
        p = Protocole(
            molecule="Gentamicine",
            dose_initiale="6-7 mg/kg",
        )
        assert p.reinjection is None
        assert p.duree is None

    def test_intention_optionnelle(self):
        p = Protocole(
            molecule="Clindamycine",
            dose_initiale="900mg IVL",
            intention=1,
        )
        assert p.intention == 1

    def test_intention_none_par_defaut(self):
        p = Protocole(
            molecule="Céfazoline",
            dose_initiale="2g IVL",
        )
        assert p.intention is None


class TestForceRecommandation:
    def test_valeurs_enum(self):
        assert ForceRecommandation.AVIS_EXPERTS == "Avis d'experts"
        assert ForceRecommandation.GRADE_1 == "GRADE 1"
        assert ForceRecommandation.GRADE_2 == "GRADE 2"

    def test_enum_depuis_string(self):
        assert ForceRecommandation("GRADE 1") == ForceRecommandation.GRADE_1


class TestIntervention:
    def test_intervention_avec_protocole(self):
        interv = Intervention(
            id="test-abp",
            nom="Test avec ABP",
            specialite="Test",
            protocole=Protocole(
                molecule="Céfazoline",
                dose_initiale="2g IVL",
                duree="Durée de l'intervention",
            ),
            force_recommandation=ForceRecommandation.AVIS_EXPERTS,
            source_page=73,
            source_tableau="Tableau test",
        )
        assert interv.protocole is not None

    def test_intervention_sans_protocole(self):
        interv = Intervention(
            id="test-sans-abp",
            nom="Test sans ABP",
            specialite="Test",
            force_recommandation=ForceRecommandation.GRADE_2,
            source_page=74,
            source_tableau="Tableau test",
        )
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

    def test_coherence_protocole_alternative(self, rfe_data: RFEData):
        """Si protocole est None → alternative_allergie est aussi None."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                if interv.protocole is None:
                    assert interv.alternative_allergie is None, (
                        f"{interv.id}: pas de protocole mais alternative_allergie renseignée"
                    )

    def test_force_recommandation_valeurs(self, rfe_data: RFEData):
        """Toutes les valeurs sont des ForceRecommandation valides (garanti par l'Enum)."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                assert isinstance(interv.force_recommandation, ForceRecommandation), (
                    f"{interv.id}: force_recommandation '{interv.force_recommandation}' inattendue"
                )

    def test_source_page_positive(self, rfe_data: RFEData):
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                assert interv.source_page > 0, f"{interv.id}: source_page={interv.source_page}"

    def test_molecule_sont_des_enum(self, rfe_data: RFEData):
        """Toutes les molécules sont des Molecule valides (garanti par le StrEnum)."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                if interv.protocole:
                    assert isinstance(interv.protocole.molecule, Molecule), (
                        f"{interv.id}: molecule '{interv.protocole.molecule}' inattendue"
                    )

    def test_intentions_alternatives_ordonnees(self, rfe_data: RFEData):
        """Les alternatives allergie ont des intentions séquentielles (1, 2, 3, ...)."""
        for spec in rfe_data.specialites:
            for interv in spec.interventions:
                if interv.alternative_allergie:
                    intentions = [alt.intention for alt in interv.alternative_allergie]
                    assert intentions == list(range(1, len(intentions) + 1)), (
                        f"{interv.id}: intentions {intentions} non séquentielles"
                    )


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
        assert pth.protocole is not None
        assert pth.protocole.molecule == Molecule.CEFAZOLINE
        assert pth.alternative_allergie is not None
        # 3 alternatives : Clindamycine (1), Vancomycine (2), Teicoplanine (3)
        assert len(pth.alternative_allergie) == 3
        assert pth.alternative_allergie[0].molecule == Molecule.CLINDAMYCINE
        assert pth.alternative_allergie[0].intention == 1
        assert pth.alternative_allergie[1].molecule == Molecule.VANCOMYCINE
        assert pth.alternative_allergie[1].intention == 2
        assert pth.alternative_allergie[2].molecule == Molecule.TEICOPLANINE
        assert pth.alternative_allergie[2].intention == 3

    def test_arthroscopie_sans_materiel_pas_de_protocole(self, rfe_data: RFEData):
        """L'arthroscopie diagnostique sans matériel n'a pas de protocole."""
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
        assert arthro.protocole is None

    def test_gustilo_2_3_amoxicilline(self, rfe_data: RFEData):
        """Les fractures ouvertes Gustilo 2-3 utilisent Amoxicilline/Clavulanate."""
        trauma = next(s for s in rfe_data.specialites if s.id == "traumatologie")
        gustilo23 = next(i for i in trauma.interventions if "gustilo 2" in i.nom.lower())
        assert gustilo23.protocole is not None
        assert "Amoxicilline" in gustilo23.protocole.molecule
