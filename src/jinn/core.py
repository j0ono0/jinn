""" Central file for control of all aspects of package. 
"""

import os
import shutil
import markdown
import jinja2
from . import settings


def copy_dir(src, dst):

    dst.mkdir(parents=True, exist_ok=True)

    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            copy_dir(s, d)
        else:
            shutil.copy2(str(s), str(d))


def update_settings(settings_dict):
    """Update application settings via a dict.
    These settings are used for navigating the source and build file system structures.
    """
    for key, val in settings_dict.items():
        setattr(settings, key, val)


class Generator:
    """Central class for controlling and assisting with the build process of the site.
    Note that an instance of this class must exist *before* a user can reference
    templates and functions of it in their site configuration file.
    """

    print(
        """
        -----------------------------------------------------------------------------
                              "Your wish is my command." --jinn                      
        -----------------------------------------------------------------------------
        """
    )

    def __init__(self, jinja_environment=None):
        self.jinja_environment = jinja_environment

        self.init_jinja_environment()

    def init_jinja_environment(self):
        if not self.jinja_environment:
            self.jinja_environment = jinja2.Environment(
                loader=jinja2.ChoiceLoader(
                    [
                        jinja2.FileSystemLoader(settings.TEMPLATE_PATH),
                        jinja2.PackageLoader("jinn", "templates"),
                    ]
                ),
                autoescape=jinja2.select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )

    def template(self, name):
        return self.jinja_environment.get_template(name)

    def copy_directories(self, src, dst):
        dst.mkdir(parents=True, exist_ok=True)
        for item in os.listdir(src):
            s = src / item
            d = dst / item
            if s.is_dir():
                copy_dir(s, d)
            else:
                shutil.copy2(str(s), str(d))

    def parse_md_file(self, path):
        path = settings.CONTENT_PATH / path
        md = markdown.Markdown(extensions=["meta"])
        with open(path) as f:
            html = {"content": md.convert(f.read())}
            meta = {k: ", ".join(v) for (k, v) in md.Meta.items()}
            return {**html, **meta}

    def build_static_directories(self):
        settings.BUILD_PATH.mkdir(parents=True, exist_ok=True)
        for dirpath, dirs, files in settings.TEMPLATE_PATH.walk():
            s = dirpath / "static"
            if s.is_dir():
                rel_path = dirpath.relative_to(settings.TEMPLATE_PATH)
                d = settings.STATIC_PATH / rel_path
                self.copy_directories(s, d)

    def build_media_directories(self):
        settings.BUILD_PATH.mkdir(parents=True, exist_ok=True)
        for dirpath, dirs, files in settings.CONTENT_PATH.walk():
            s = dirpath / "media"
            if s.is_dir():
                rel_path = dirpath.relative_to(settings.CONTENT_PATH)
                d = settings.MEDIA_PATH / rel_path
                self.copy_directories(s, d)

    def build_page(self, page):
        #  used for formatting html_tag.jinja
        page["_helpers"] = {
            "void_tags": [
                "area",
                "base",
                "br",
                "col",
                "embed",
                "hr",
                "img",
                "input",
                "link",
                "meta",
                "param",
                "source",
                "track",
                "wbr",
            ]
        }

        with open(settings.BUILD_PATH / page["slug"], "w") as f:
            f.write(page["template"].render(page))
