# qchem_inputgen
Lightweight Python tool to generate Q-Chem input files from XYZ geometries, with defaults tailored for MRSF calculations and a clean CLI interface.

## qchem_inputgen

qchem_inputgen is a lightweight, object-oriented Python tool for generating
Q-Chem input files directly from XYZ geometry files.

The tool is designed to streamline the preparation of electronic-structure
calculations by providing sensible defaults for MRSF-TDDFT calculations, while
allowing full customization through a simple command-line interface.

The repository is intentionally simple: users can clone it and run the tool
immediately, without requiring conda environments or external dependencies.


## Motivation

Preparing Q-Chem input files repeatedly for different molecules, spin states,
and density functionals is error-prone and time-consuming. This tool automates
that process by:

- Reading standard XYZ geometry files
- Generating consistent $molecule and $rem sections
- Enforcing clean defaults suitable for MRSF calculations
- Allowing flexible overrides for common Q-Chem keywords

The design emphasizes clarity, extensibility, and reproducibility, making the
tool suitable for both individual research workflows and group-wide use.


## Key Features


- Generate Q-Chem input files directly from .xyz geometries
- Sensible defaults for MRSF single-point calculations
- Support for batch processing of multiple XYZ files or directories
- Fully configurable via command-line options:
  * charge
  * spin multiplicity
  * DFT functional
  * basis set
  * job type
  * Molden output
  * orbital printing
- Clean object-oriented design for easy extension
- No external dependencies beyond standard Python (>= 3.10)


## Default Settings


Unless overridden via command-line options, the following defaults are used:

| Keyword        | Default |
|---------------|---------|
| JOB_TYPE      | sp      |
| METHOD        | mrsf    |
| EXCHANGE      | bhhlyp  |
| BASIS         | 6-31G*  |
| CHARGE        | 0       |
| MULTIPLICITY  | 1       |
| MOLDEN_FORMAT | TRUE    |


These defaults are chosen to reflect common usage patterns for MRSF-TDDFT
energy calculations.


## Repository Structure

```text
qchem_inputgen/
├── README.md
├── LICENSE
├── pyproject.toml
├── scripts/
│   └── qchem_inputgen
├── src/
│   └── qchem_inputgen/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── qchem.py
│       └── xyz.py
└── tests/
    ├── test_render.py
    └── test_xyz.py
```

## Design Overview

`xyz.py`  
  Responsible for parsing and validating XYZ geometry files.

`qchem.py`  
  Defines Q-Chem input options and renders the $molecule and $rem blocks.

`cli.py`  
  Implements the command-line interface and orchestrates the workflow.

`__main__.py`  
  Enables execution via `python -m qchem_inputgen`.

`scripts/qchem_inputgen`  
  Standalone executable launcher for users who do not wish to install the
  package.


## Installation

No installation is required for basic usage.

Simply clone the repository:

  `git clone git@github.com:achakra9/qchem_inputgen.git`  
  `cd qchem_inputgen`

Python 3.10 or newer is recommended.


## Usage

Option 1: Run as a Python module (recommended)

  `python -m qchem_inputgen molecule.xyz -o inputs/`


Option 2: Run the standalone script

  `./scripts/qchem_inputgen molecule.xyz -o inputs/`


Option 3: Optional editable install (for convenience only)

  `pip install -e .`  
  `qchem_inputgen molecule.xyz -o inputs/`


## Examples

Basic usage (defaults):

  `python -m qchem_inputgen h2o.xyz`

This generates:

  `h2o.in`

with METHOD=mrsf, EXCHANGE=bhhlyp, BASIS=6-31G*, charge=0, and multiplicity=1.


Specify charge and multiplicity:

  `python -m qchem_inputgen o2.xyz --charge 0 --mult 3`


Change functional and basis set:

  `python -m qchem_inputgen mol.xyz --functional pbe0 --basis def2-svp`


Process an entire directory of XYZ files:

  `python -m qchem_inputgen geometries/ -o inputs/`


Enable orbital printing and disable Molden output:

  `python -m qchem_inputgen mol.xyz --print-orbitals --no-molden`


## Output Format

Each XYZ file produces a Q-Chem input file with the same base name:

  `molecule.xyz  ->  molecule.in`

The generated input contains:
- A $molecule block with charge, multiplicity, and Cartesian coordinates
- A $rem block with user-specified or default keywords


<!-- ## Extending the Tool

The code is intentionally modular and easy to extend. Common extensions include:

- Adding MRSF-specific control keywords
- Supporting excited-state or gradient calculations
- Reading settings from a YAML or JSON configuration file
- Inferring charge or multiplicity from file names
- Adding job templates for properties or response calculations -->

## Intended Audience

This tool is intended for:

- Researchers using Q-Chem for electronic-structure calculations
- Developers working on method implementations (e.g., MRSF-TDDFT)
- Users who want reproducible and standardized input generation
- Students learning best practices in scientific Python scripting


## License

This project is released under the MIT License.


## Author

Arnab Chakraborty  
Postdoctoral Research Associate  
University of Southern California  
email: arnabc20@usc.edu  


## Disclaimer

This tool generates Q-Chem input files but does not validate keyword
compatibility with specific Q-Chem versions. Users are responsible for ensuring
that generated inputs are appropriate for their installed Q-Chem version and
licensing.

