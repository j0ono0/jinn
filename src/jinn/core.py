import os
import shutil
import markdown
import jinja2
from . import settings

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


def update_settings(settings_dict):
    for key, val in settings_dict.items():
        setattr(settings, key, val)


class Generator:

    def __init__(self, jinja_environment=None):
        self.templates = None
        self.jinja_environment(jinja_environment)

    def jinja_environment(self, jinja_environment=None):
        if type(jinja_environment) != jinja2.Environment:
            self.templates = jinja2.Environment(
                loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH),
                autoescape=jinja2.select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
        else:
            self.templates = jinja_environment

    def template(self, name):
        return self.templates.get_template(name)

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
