import argparse
from pathlib import Path
from jinn import settings

parser = argparse.ArgumentParser(
    description="""Command jinn to generate a static site. 
        Note: This tool is expected to be run from the project source folder."""
)

parser.add_argument("src", type=str, help="source file to control build process")
parser.add_argument(
    "-b",
    "--build",
    type=str,
    help="Build folder for site to be built into. Omitted the project builds into './build'.",
)

args = parser.parse_args()
src = Path(args.src)
if args.build:
    dst = Path(args.build)
else:
    dst = Path(".").parent / "build"


# Validate input ######################################################################

if not src.is_file():
    raise ValueError(
        """
        The source path must be to a file.
        """
    )

if dst.is_file():
    raise ValueError(
        """
        The destination path must be a folder.
        """
    )

# Import user defined Python module #####################################################
import importlib
import sys
import os

settings.BUILD_PATH = dst.resolve()

here = Path(".")

if here == src.parent:
    # in project root
    #######################################
    # This only works from the project root
    spec = importlib.util.spec_from_file_location(src.stem, src)
    module = importlib.util.module_from_spec(spec)
    sys.modules[src.stem] = module
    spec.loader.exec_module(module)

else:
    raise ValueError(
        """This command can be run from the project root folder only.
        """
    )
