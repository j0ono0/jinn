# Application settings and default values.

from pathlib import Path

# Source folders.
# Template and content folders are concatenated with
# PROJ_ROOT to find source files where explicit paths are not supplied.
PROJ_ROOT = Path(".").resolve()
TEMPLATE_SOURCE = "templates"
CONTENT_SOURCE = "content"

# Destination folders.
# Static and media folders are concatenated with
# BUILD_ROOT to create an output files destination where explicit paths are not supplied.
BUILD_ROOT = None
STATIC_DESTINATION = "assets"
MEDIA_DESTINATION = "media"
