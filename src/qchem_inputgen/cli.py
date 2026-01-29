from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from .qchem import QChemInputWriter, QChemOptions
from .xyz import XYZReader


class InputGenerator:
    def __init__(self) -> None:
        self.reader = XYZReader()
        self.writer = QChemInputWriter()

    def expand_xyz(self, items: List[str]) -> List[Path]:
        xyz_files: List[Path] = []
        for s in items:
            p = Path(s)
            if p.is_dir():
                xyz_files.extend(sorted(p.glob("*.xyz")))
            else:
                xyz_files.append(p)
        return xyz_files

    def generate(
        self,
        xyz_files: List[Path],
        outdir: Path,
        *,
        charge: int,
        mult: int,
        opts: QChemOptions,
        suffix: str,
    ) -> List[Path]:
        written: List[Path] = []
        for xyz_path in xyz_files:
            mol = self.reader.read(xyz_path, charge=charge, multiplicity=mult)
            title = f"{xyz_path.stem}/{opts.basis}/{opts.exchange} MRSF-TDDFT"
            text = self.writer.render(mol, opts, title=title)
            outpath = outdir / f"{xyz_path.stem}{suffix}"
            outpath.write_text(text)
            written.append(outpath)
        return written


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="qchem_inputgen",
        description="Generate Q-Chem input files using an MRSF/SF-CIS template.",
    )
    p.add_argument("xyz", nargs="+", help="XYZ file(s) or directories.")
    p.add_argument("-o", "--outdir", default=".", help="Output directory.")
    p.add_argument("--suffix", default=".in", help="Output suffix.")
    p.add_argument("--charge", type=int, default=0, help="Total charge.")
    p.add_argument("--mult", type=int, default=3, help="Spin multiplicity.")

    p.add_argument("--basis", default="6-31G*", help="Basis set.")
    p.add_argument("--exchange", default="BHHLYP", help="DFT exchange functional.")

    p.add_argument("--unrestricted", action="store_true", help="Set unrestricted TRUE.")
    p.add_argument("--scf-guess", default="CORE")
    p.add_argument("--scf-convergence", type=int, default=10)
    p.add_argument("--scf-algorithm", default="DIIS")
    p.add_argument("--max-scf-cycles", type=int, default=100)

    p.add_argument("--spin-flip", type=int, default=2)
    p.add_argument("--cis-n-roots", type=int, default=4)
    p.add_argument("--singlets", action="store_true", default=True)
    p.add_argument("--triplets", action="store_true", default=False)
    p.add_argument("--cis-convergence", type=int, default=8)
    p.add_argument("--max-cis-cycles", type=int, default=100)
    p.add_argument("--no-sts-mom", action="store_true")
    p.add_argument("--no-comment", action="store_true")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    opts = QChemOptions(
        basis=args.basis,
        exchange=args.exchange,
        unrestricted=args.unrestricted,
        scf_guess=args.scf_guess,
        scf_convergence=args.scf_convergence,
        scf_algorithm=args.scf_algorithm,
        max_scf_cycles=args.max_scf_cycles,
        spin_flip=args.spin_flip,
        cis_n_roots=args.cis_n_roots,
        cis_singlets=args.singlets,
        cis_triplets=args.triplets,
        cis_convergence=args.cis_convergence,
        max_cis_cycles=args.max_cis_cycles,
        sts_mom=not args.no_sts_mom,
        include_comment=not args.no_comment,
    )

    gen = InputGenerator()
    xyz_files = gen.expand_xyz(args.xyz)
    if not xyz_files:
        raise SystemExit("No XYZ files found.")

    for p in gen.generate(
        xyz_files,
        outdir,
        charge=args.charge,
        mult=args.mult,
        opts=opts,
        suffix=args.suffix,
    ):
        print(f"Wrote {p}")

    return 0
