import argparse
from pathlib import Path
import sys
from jinn import settings, core


parser = argparse.ArgumentParser(
    description="""Command jinn to generate a static site. 
        Note: this must be run from the source folder if you have submobules."""
)

parser.add_argument("src", type=str, help="source file to control build process")
parser.add_argument(
    "dst", type=str, help="destination folder for site to be built into."
)

args = parser.parse_args()
src = Path(args.src)
dst = Path(args.dst)


# Validate input ######################################################################

if not src.is_file():
    raise argparse.ArgumentError("The source path must be to a file.")

if dst.is_file():
    raise argparse.ArgumentError("The destination path must be a folder.")


# Import user defined Python file #####################################################

import importlib.util
import sys

spec = importlib.util.spec_from_file_location(src.stem, src)
module = importlib.util.module_from_spec(spec)
sys.modules[src.stem] = module
try:
    spec.loader.exec_module(module)
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        """
        ------------------------------------------------------------------------------
        Run this CLI tool from the source directory if you have 'ModuleNotFoundError'.
        It is due to a Python import limitation. 
        ------------------------------------------------------------------------------
        """
    )
