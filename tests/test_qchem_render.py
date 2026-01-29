from pathlib import Path

from qchem_inputgen.xyz import XYZReader
from qchem_inputgen.qchem import QChemOptions, QChemInputWriter


def make_be(tmp_path: Path):
    xyz = tmp_path / "be.xyz"
    xyz.write_text(
        "1\n"
        "Be atom\n"
        "Be 0.0 0.0 0.0\n"
    )
    return XYZReader().read(xyz, charge=0, multiplicity=3)


def test_render_contains_required_blocks(tmp_path: Path) -> None:
    mol = make_be(tmp_path)
    text = QChemInputWriter().render(
        mol, QChemOptions(), title="Be/6-31G*/BHHLYP MRSF-TDDFT"
    )

    assert "$comment" in text
    assert "$molecule" in text
    assert "$rem" in text


def test_exchange_keyword_used(tmp_path: Path) -> None:
    mol = make_be(tmp_path)
    opts = QChemOptions(exchange="BHHLYP")
    text = QChemInputWriter().render(mol, opts)

    assert "EXCHANGE           BHHLYP" in text


def test_spin_flip_and_cis_keywords(tmp_path: Path) -> None:
    mol = make_be(tmp_path)
    text = QChemInputWriter().render(mol, QChemOptions())

    assert "SPIN_FLIP" in text
    assert "CIS_N_ROOTS" in text
    assert "CIS_SINGLETS" in text
    assert "CIS_TRIPLETS" in text


def test_boolean_toggles(tmp_path: Path) -> None:
    mol = make_be(tmp_path)
    opts = QChemOptions(
        cis_singlets=False,
        cis_triplets=True,
    )
    text = QChemInputWriter().render(mol, opts)

    assert "CIS_SINGLETS       FALSE" in text
    assert "CIS_TRIPLETS       TRUE" in text
