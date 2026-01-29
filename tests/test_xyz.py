from pathlib import Path
import pytest

from qchem_inputgen.xyz import XYZReader


def test_read_xyz_valid(tmp_path: Path) -> None:
    xyz = tmp_path / "be.xyz"
    xyz.write_text(
        "1\n"
        "Be atom\n"
        "Be 0.0 0.0 0.0\n"
    )

    mol = XYZReader().read(xyz, charge=0, multiplicity=3)

    assert mol.charge == 0
    assert mol.multiplicity == 3
    assert len(mol.atoms) == 1
    assert mol.atoms[0][0] == "Be"


def test_read_xyz_missing_file(tmp_path: Path) -> None:
    reader = XYZReader()
    with pytest.raises(FileNotFoundError):
        reader.read(tmp_path / "missing.xyz", charge=0, multiplicity=1)


def test_read_xyz_bad_atom_count(tmp_path: Path) -> None:
    xyz = tmp_path / "bad.xyz"
    xyz.write_text(
        "2\n"
        "comment\n"
        "H 0.0 0.0 0.0\n"
    )

    with pytest.raises(ValueError):
        XYZReader().read(xyz, charge=0, multiplicity=1)
