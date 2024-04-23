import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Command jinn to generate a static site.")

parser.add_argument("src", type=str, help="source file to control build process")
parser.add_argument(
    "dst", type=str, help="destination folder for site to be built into."
)

args = parser.parse_args()
src = Path(args.src)
dst = Path(args.dst)

if not src.is_file():
    raise argparse.ArgumentError("The source path must be to a file.")

if dst.is_file():
    raise argparse.ArgumentError("The destination path must be a folder.")

print(src)
for f in dst.iterdir():
    print(f)
