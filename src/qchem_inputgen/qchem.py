from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .xyz import Molecule


@dataclass(frozen=True)
class QChemOptions:
    """
    Q-Chem default options for an MRSF-style calculation.

    This matches the user's default template:

      JOBTYPE            SP
      UNRESTRICTED       FALSE
      BASIS              6-31G*
      EXCHANGE           BHHLYP
      SCF_GUESS          CORE
      SCF_CONVERGENCE    10
      SCF_ALGORITHM      DIIS
      MAX_SCF_CYCLES     100
      SPIN_FLIP          2
      CIS_N_ROOTS        4
      CIS_SINGLETS       TRUE
      CIS_TRIPLETS       FALSE
      CIS_CONVERGENCE    8
      MAX_CIS_CYCLES     100
    """

    # Core job controls
    jobtype: str = "SP"
    unrestricted: bool = False

    # DFT and basis
    basis: str = "6-31G*"
    exchange: str = "BHHLYP"  

    # SCF controls
    scf_guess: str = "CORE"
    scf_convergence: int = 10
    scf_algorithm: str = "DIIS"
    max_scf_cycles: int = 100

    # MRSF/SF-CIS controls
    spin_flip: int = 2
    cis_n_roots: int = 4
    cis_singlets: bool = True
    cis_triplets: bool = False
    cis_convergence: int = 8
    max_cis_cycles: int = 100

    # Comment block
    include_comment: bool = True


class QChemInputWriter:
    """Render a Q-Chem input file from a Molecule + QChemOptions, matching the given template."""

    @staticmethod
    def _tf(x: bool) -> str:
        return "TRUE" if x else "FALSE"

    @staticmethod
    def _kv(key: str, value: str, width: int = 18) -> str:
        # Create aligned key/value lines similar to the template
        return f"{key:<{width}} {value}"

    def render(self, mol: Molecule, opts: QChemOptions, *, title: Optional[str] = None) -> str:
        """
        Create the full Q-Chem input text with:
        - $comment ... $end
        - $molecule ... $end
        - $rem ... $end

        Parameters
        ----------
        title : Optional[str]
            If provided, used in $comment line 1. If omitted, a default title is generated.
        """
        blocks: List[str] = []

        # $comment block
        if opts.include_comment:
            # If no explicit title, generate something like: "<name>/<basis>/<exchange> MRSF-TDDFT"
            # "name" can be supplied by caller (usually xyz stem).
            auto_title = title if title else f"{opts.basis}/{opts.method} MRSF-TDDFT"
            comment_lines = [
                "$comment",
                f"  1 {auto_title}",
                "  2",
                "$end",
                "",
            ]
            blocks.append("\n".join(comment_lines))

        # $molecule block
        mol_lines: List[str] = ["$molecule", f"{mol.charge} {mol.multiplicity}"]
        for sym, x, y, z in mol.atoms:
            mol_lines.append(f"{sym:<2s}  {x:12.6f}  {y:12.6f}  {z:12.6f}")
        mol_lines.append("$end")
        blocks.append("\n".join(mol_lines) + "\n")

        # $rem block
        rem: List[str] = ["$rem"]
        rem.append(self._kv("JOBTYPE", opts.jobtype))
        rem.append(self._kv("UNRESTRICTED", self._tf(opts.unrestricted)))
        rem.append(self._kv("BASIS", opts.basis))
        rem.append(self._kv("METHOD", opts.method))
        rem.append(self._kv("SCF_GUESS", opts.scf_guess))
        rem.append(self._kv("SCF_CONVERGENCE", str(opts.scf_convergence)))
        rem.append(self._kv("SCF_ALGORITHM", opts.scf_algorithm))
        rem.append(self._kv("MAX_SCF_CYCLES", str(opts.max_scf_cycles)))
        rem.append(self._kv("SPIN_FLIP", str(opts.spin_flip)))
        rem.append(self._kv("CIS_N_ROOTS", str(opts.cis_n_roots)))
        rem.append(self._kv("CIS_SINGLETS", self._tf(opts.cis_singlets)))
        rem.append(self._kv("CIS_TRIPLETS", self._tf(opts.cis_triplets)))
        rem.append(self._kv("CIS_CONVERGENCE", str(opts.cis_convergence)))
        rem.append(self._kv("MAX_CIS_CYCLES", str(opts.max_cis_cycles)))
        # add more if needed
        rem.append("$end")

        blocks.append("\n".join(rem) + "\n")

        return "\n".join(blocks)
