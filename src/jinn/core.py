import os
import shutil
from pathlib import Path
import markdown
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)


print("jinn imported. your wish is my command")


def copy_dir(src, dst):

    dst.mkdir(parents=True, exist_ok=True)

    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            copy_dir(s, d)
        else:
            shutil.copy2(str(s), str(d))


class Generator:

    def __init__(self, config):
        self.config = config

    def copy_directories(self, src, dst):
        dst.mkdir(parents=True, exist_ok=True)
        for item in os.listdir(src):
            s = src / item
            d = dst / item
            if s.is_dir():
                copy_dir(s, d)
            else:
                shutil.copy2(str(s), str(d))

    def copy_static_directories(self):

        self.config["BUILD_PATH"].mkdir(parents=True, exist_ok=True)

        for dirpath, dirs, files in self.config["TEMPLATE_PATH"].walk():
            s = dirpath / "static"
            if s.is_dir():
                rel_path = dirpath.relative_to(self.config["TEMPLATE_PATH"])
                d = self.config["STATIC_ROOT"] / rel_path
                self.copy_directories(s, d)
