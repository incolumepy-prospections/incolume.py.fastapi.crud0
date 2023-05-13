"""
Principal Module.

Update metadata from version by semver
"""
from pathlib import Path

from tomli import load

configfile = Path(__file__).parents[4].joinpath("pyproject.toml")
versionfile = Path(__file__).parent.joinpath("version.txt")

with configfile.open("rb") as f:
    versionfile.write_text(f"{load(f)['tool']['poetry']['version']}\n")

__version__ = versionfile.read_text().strip()


if __name__ == "__main__":
    print(__version__)
