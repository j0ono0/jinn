import argparse
from pathlib import Path


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


here = Path(".")

if here == src.parent:
    # in project root
    modulepath = src.stem
elif src.resolve().is_relative_to(here.resolve()):
    # user above above
    modulepath = ".".join(src.parent.joinpath(src.stem).as_posix().split("/"))
else:
    pathup = src.parent.relative_to(Path("."))
    upcount = len(pathup.as_posix().split("/"))
    modulepath = f'{'.'*upcount}{src.stem}'

print(modulepath)

sys.path.append(src.parent.resolve())


#######################################
#######################################

# This only works from the project root

#######################################
#######################################

spec = importlib.util.spec_from_file_location(src.stem, src)
module = importlib.util.module_from_spec(spec)
sys.modules[src.stem] = module
spec.loader.exec_module(module)

# import from outside user module
# module = importlib.import_module('site01.site')
# print(dir(module))
