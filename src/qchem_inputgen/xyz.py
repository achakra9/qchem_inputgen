from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class Molecule:
    """Immutable container for a molecule parsed from an XYZ file."""
    charge: int
    multiplicity: int
    atoms: List[Tuple[str, float, float, float]]  # (symbol, x, y, z)


class XYZReader:
    """Read and validate XYZ files."""

    def read(self, path: str | Path, *, charge: int = 0, multiplicity: int = 1) -> Molecule:
        """
        Parse an XYZ file into a Molecule object.

        XYZ format:
          line 1: number of atoms (int)
          line 2: comment (ignored)
          line 3+: atom lines:  Symbol  x  y  z

        Empty lines are ignored.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"XYZ file not found: {path}")

        lines = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
        if len(lines) < 3:
            raise ValueError(f"Invalid XYZ (too few lines): {path}")

        try:
            n_atoms = int(lines[0])
        except ValueError as e:
            raise ValueError(f"Invalid XYZ first line (expected atom count): {path}") from e

        atom_lines = lines[2:]
        if len(atom_lines) < n_atoms:
            raise ValueError(
                f"XYZ atom count mismatch in {path}: expected {n_atoms}, got {len(atom_lines)}"
            )

        atoms: List[Tuple[str, float, float, float]] = []
        for i in range(n_atoms):
            parts = atom_lines[i].split()
            if len(parts) < 4:
                raise ValueError(f"Invalid atom line {i+3} in {path}: '{atom_lines[i]}'")

            sym = parts[0]
            try:
                x, y, z = map(float, parts[1:4])
            except ValueError as e:
                raise ValueError(f"Invalid coordinates on line {i+3} in {path}: '{atom_lines[i]}'") from e

            atoms.append((sym, x, y, z))

        return Molecule(charge=charge, multiplicity=multiplicity, atoms=atoms)
