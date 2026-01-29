from pathlib import Path
import subprocess
import sys


def test_cli_generates_input(tmp_path: Path) -> None:
    xyz = tmp_path / "be.xyz"
    xyz.write_text(
        "1\n"
        "Be atom\n"
        "Be 0.0 0.0 0.0\n"
    )

    outdir = tmp_path / "out"
    outdir.mkdir()

    cmd = [
        sys.executable,
        "-m",
        "qchem_inputgen",
        str(xyz),
        "-o",
        str(outdir),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    out_file = outdir / "be.in"
    assert out_file.exists()

    text = out_file.read_text()
    assert "$molecule" in text
    assert "$rem" in text
