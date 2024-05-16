import argparse
import http.server
import socketserver
from pathlib import Path
from jinn import settings


def generate_site(args):
    if args.src == None:
        raise ValueError(
            """
            Source file missing. eg: py -m jinn generate --src mysite.py
            """
        )

    src = Path(args.src)
    dst = Path(args.dst)

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

    settings.BUILD_DESTINATION = dst.resolve()

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


def build_with_theme(args):
    from jinn.themes.simple_site import simple_site

    simple_site.build()


def run_dev_server(args):
    PORT = args.port

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


parser = argparse.ArgumentParser(
    description="""Command jinn to generate a static site. 
        Note: This tool is expected to be run from the project source folder.""",
)
parser.add_argument(
    "command",
    choices=["generate", "devserver", "build"],
    help="The first argument must be a valid command.",
)

parser.add_argument(
    "-s",
    "--src",
    type=str,
    help="Source .py file to control generator processes, or source folder if using 'build' command",
)
parser.add_argument(
    "-d",
    "--dst",
    type=str,
    default="./build",
    help="Destination folder. If omitted detfaults to '.build'.",
)

parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=8000,
    help="Port to run development server on.",
)

parser.add_argument(
    "-t",
    "--theme",
    type=str,
    choices=["simple_site", "simple"],
    help="Use a theme builder",
)

args = parser.parse_args()

commands = {
    "generate": generate_site,
    "devserver": run_dev_server,
    "build": build_with_theme,
}

commands[args.command.lower()](args)
