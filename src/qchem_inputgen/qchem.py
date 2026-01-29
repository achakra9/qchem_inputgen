from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .xyz import Molecule


@dataclass(frozen=True)
class QChemOptions:
    """
    Q-Chem options matching the default SF/MRSF-style template.

    """

    # Core
    jobtype: str = "SP"
    unrestricted: bool = False

    # DFT + basis
    basis: str = "6-31G*"
    exchange: str = "BHHLYP"

    # SCF
    scf_guess: str = "CORE"
    scf_convergence: int = 10
    scf_algorithm: str = "DIIS"
    max_scf_cycles: int = 100

    # SF/MRSF CIS controls
    spin_flip: int = 2
    cis_n_roots: int = 4
    cis_singlets: bool = True
    cis_triplets: bool = False
    cis_convergence: int = 8
    max_cis_cycles: int = 100
    sts_mom: bool = True

    # Comment block
    include_comment: bool = True


class QChemInputWriter:
    """Render a Q-Chem input file from Molecule + QChemOptions."""

    @staticmethod
    def _tf(x: bool) -> str:
        return "TRUE" if x else "FALSE"

    @staticmethod
    def _kv(key: str, value: str, width: int = 18) -> str:
        return f"{key:<{width}} {value}"

    def render(self, mol: Molecule, opts: QChemOptions, *, title: Optional[str] = None) -> str:
        blocks: List[str] = []

        # $comment
        if opts.include_comment:
            auto_title = title if title else f"{opts.basis}/{opts.exchange} MRSF-TDDFT"
            blocks.append(
                "\n".join(
                    [
                        "$comment",
                        f"  1 {auto_title}",
                        "  2",
                        "$end",
                        "",
                    ]
                )
            )

        # $molecule
        mol_lines: List[str] = ["$molecule", f"{mol.charge} {mol.multiplicity}"]
        for sym, x, y, z in mol.atoms:
            mol_lines.append(f"{sym:<2s}  {x:12.6f}  {y:12.6f}  {z:12.6f}")
        mol_lines.append("$end")
        blocks.append("\n".join(mol_lines) + "\n")

        # $rem
        rem: List[str] = ["$rem"]
        rem.append(self._kv("jobtype", opts.jobtype))
        rem.append(self._kv("unrestricted", self._tf(opts.unrestricted)))
        rem.append(self._kv("basis", opts.basis))
        rem.append(self._kv("EXCHANGE", opts.exchange))
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
        rem.append(self._kv("sts_mom", "true" if opts.sts_mom else "false"))
        rem.append("$end")
        blocks.append("\n".join(rem) + "\n")

        return "\n".join(blocks)
