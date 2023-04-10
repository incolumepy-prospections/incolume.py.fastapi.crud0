"""Principal Module."""
import logging
from pathlib import Path

try:
    from tomllib import load
except (ModuleNotFoundError, ImportError):
    from tomli import load


__author__ = "@britodfbr"

configfile = Path(__file__).parents[4].joinpath("pyproject.toml")
versionfile = Path(__file__).parent.joinpath("version.txt")

with configfile.open('rb') as file:
        versionfile.write_text(
             f"{load(file)['tool']['poetry']['version']}\n")

__version__ = versionfile.read_text().strip()

if __name__ == "__main__":
    logging.debug('%s, %s %s', configfile, versionfile)
    logging.debug('Vesion load: %s', __version__)
