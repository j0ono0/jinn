# Helper function that do not rely on content stored in jinn.Generator instance

import json
import os
from pathlib import Path
import shutil
import markdown


def copy_directory(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            copy_directory(s, d)
        else:
            shutil.copy2(str(s), str(d))


def parse_md_file(path, delimiter=" "):
    md = markdown.Markdown(extensions=["meta"])
    with open(path) as f:
        html = md.convert(f.read())
        meta = md.Meta
    if delimiter:
        meta = {k: delimiter.join(v) for (k, v) in md.Meta.items()}
        return {"content": html, "meta": meta}


def confirm_metafile_update(metafile):
    # TODO: do further checks
    # - meta file have newest mtime
    # - all files are in meta with no additions/removals
    if metafile.is_file():
        user_response = input("This meta file already exists. Overwrite anyway? (y/n)")
        if user_response in ["n", "N", "no", "No"]:
            return False
    return True


def collate_markdown_meta(src, dst=None, delimiter=" ", confirm_overwrite=None):
    """Collate the meta content from all markdown files found in the 'src' folder.
    If a destination path is provided, the data is saved to that location in JSON format.
    If 'dst' is a folder a file name will be created '<folder name>_meta.json'. If a pre-existing file
    is at the destination, data from that file will be updated with meta data from the .md files.
    Additional data is retained on the assumption it maybe have been added via another source.
    The repercussion of this is that obselete data is not removed. Eg, deleting a meta entry in
    an .md file (or even deleting an entire .md file) and running collate_markdown_meta() does
    *NOT* remove that data from the meta data file.

    Returns a dict of collated meta data.

    src: A path to a folder.

    dst: (optional) destination path for collated meta data to be saved to in JSON format

    delimiter: By default Markdown meta is returned as a list for each entry. Providing a delimiter converts the list to a string.

    confirm_overwrite: If a file already exists at 'dst' confirmation is required before that file is altered.
    Changing this argument to 'True' will skip the confirmation check.
    """

    # Validate paths and convert to Path type #####################################################

    src = Path(src)

    if dst:
        dst = Path(dst)
        # Add default dst filename if none provided
        if dst.is_dir():
            dst = dst / f"{src.stem}_meta.json"

    # Validate src path
    if not src.exists() or src.is_file():
        error_msg = "The source path is not valid. It either does not exist or is not a path to a folder."
        raise ValueError(error_msg)

    # Load and validate existing data #############################################################

    try:
        with open(dst, "r") as f:
            metadata = f.read()
            try:
                metadata = json.loads(metadata)
            except json.decoder.JSONDecodeError as e:
                print(e)
                print("the destination file exists but is not valid JSON format")
            if "articles" not in metadata:
                error_msg = "A valid destination file exists but does not include the required 'articles' attribute"
                raise ValueError(error_msg)

    except FileNotFoundError:
        metadata = {
            "modified": None,
            "articles": [],
        }

    # Extract meta from markdown files and update existing metadata ###############################

    for filename in [
        f for f in src.iterdir() if f.is_file() and Path(f).suffix == ".md"
    ]:
        meta = parse_md_file(Path(filename), delimiter)["meta"]
        meta["src"] = filename.name

        # Update existing entry if it exists or create a new one
        articlemeta = next(
            (a for a in metadata["articles"] if a["src"] == meta["src"]), None
        )
        if articlemeta:
            # Update existing entry
            articlemeta.update(meta)
        else:
            # Append new entry
            metadata["articles"].append(meta)

    # Save to destination file ####################################################################

    if dst:
        # Confirm overwrite file is okay
        if confirm_overwrite == None:
            confirm_overwrite = confirm_metafile_update(dst)

        if confirm_overwrite:
            filedata = json.dumps(metadata, indent=4)
            with open(dst, "w") as f:
                f.write(filedata)

    return metadata
