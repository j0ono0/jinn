from pathlib import Path
from jinn import core, settings
from jinn import utilities as util


def build():
    jinn = core.Generator()

    source_files = [
        f for f in jinn.content_source.iterdir() if f.is_file() and f.suffix == ".md"
    ]

    # Collect content for navigation
    # Could be used to generate site map too?
    site_nav = []
    for filepath in source_files:
        pagedata = util.parse_md_file(filepath)
        site_nav.append(
            {
                "title": pagedata["title"],
                "href": Path(util.slugify(pagedata["title"])).with_suffix(".html"),
            }
        )

    # Build pages
    for filepath in [
        f for f in jinn.content_source.iterdir() if f.is_file() and f.suffix == ".md"
    ]:
        pagedata = util.parse_md_file(filepath)
        pagedata["url"] = Path(util.slugify(pagedata["title"])).with_suffix(".html")
        pagedata["template"] = jinn.tplt("simple_site/simple_site")
        pagedata["nav"] = site_nav
        # Add mandatory metadata for page build
        jinn.build_page(pagedata)

    ########################################################
    #  TODO: copy files from package into users directory
    ########################################################

    # jinn.copy_static_directories() # <---this doesn't work**

    print(
        f"""
                         Site created with 'simple_site' theme.
                         To view the site, run a python server
                      (py -m http.server) from the location folder
        -----------------------------------------------------------------------------
        Location: {jinn.build_destination}
        -----------------------------------------------------------------------------
        """
    )
