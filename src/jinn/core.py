""" Central file for control of all aspects of package. 
"""

import jinja2
import markdown
import os
from pathlib import Path
import shutil
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


def parse_md_file(path):
    md = markdown.Markdown(extensions=["meta"])
    with open(path) as f:
        html = {"content": md.convert(f.read())}
        meta = {k: ", ".join(v) for (k, v) in md.Meta.items()}
        return {**html, **meta}


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
        from pathlib import Path

        self.init_jinja_environment()

    def init_jinja_environment(self):
        template_path = Path(settings.PROJECT_PATH) / settings.TEMPLATE_SOURCE
        if not self.jinja_environment:
            self.jinja_environment = jinja2.Environment(
                loader=jinja2.ChoiceLoader(
                    [
                        jinja2.FileSystemLoader(template_path),
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

    def copy_assets(self):
        """Copy static and media files with a single command. This convenience
        function uses destination paths configered in settings.py. For more control
        static and media directories can be copied independently
        """
        self.copy_static_directories()
        self.copy_media_directories()

    def copy_static_directories(self, destination_path=None):
        """Copy static files from source to build locations.
        Optional destination_path overrides default behaviour.
        """
        destination_path = (
            destination_path
            or Path(settings.BUILD_PATH).resolve() / settings.STATIC_DESTINATION
        )
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        template_path = Path(settings.PROJECT_PATH) / settings.TEMPLATE_SOURCE
        for dirpath, dirs, files in template_path.walk():
            s = dirpath / "static"
            if s.is_dir():
                rel_path = dirpath.relative_to(template_path)
                d = destination_path / rel_path
                self.copy_directories(s, d)

    def copy_media_directories(self, destination_path=None):
        """Copy media files from source to build locations.
        Optional destination_path overrides default behaviour.
        """
        destination_path = (
            destination_path
            or Path(settings.BUILD_PATH).resolve() / settings.MEDIA_DESTINATION
        )
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        content_path = Path(settings.PROJECT_PATH) / settings.CONTENT_SOURCE
        for dirpath, dirs, files in content_path.walk():
            s = dirpath / "media"
            if s.is_dir():
                rel_path = dirpath.relative_to(content_path)
                d = destination_path / rel_path
                self.copy_directories(s, d)

    def build_page(self, page):
        try:
            build_path = Path(page["build_directory"]) / page["url"]
        except KeyError:
            try:
                build_path = Path(settings.BUILD_PATH).resolve() / page["url"]
            except KeyError:
                msg = "'url' is a required dict attribute in data passed to Generator.build_page()."
                raise KeyError(msg)

        if not build_path:
            raise TypeError(
                """
                No destination folder has been set for the output of this page.
                The page dict needs a 'build_directory' attribute -OR- Set a 
                default BUILD_PATH in settings by adding:
                    setting.BUILD_PATH = "<absolute path to destination folder>"
                """
            )
        build_path.parent.mkdir(parents=True, exist_ok=True)
        with open(build_path, "w") as f:
            f.write(page["template"].render(page))
