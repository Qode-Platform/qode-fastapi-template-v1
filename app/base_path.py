"""The fleet's BASE_PATH contract, in one place.

nginx forwards the whole `/direct/<agent>:<port>` prefix UNCHANGED, so the app
has to serve every route under it — the prefix is NOT stripped before it
reaches us. Empty/unset means standalone mode: serve at the host root.
"""

import os


def base_path() -> str:
    """Normalised prefix: '' or '/leading/no-trailing-slash'."""
    raw = (os.getenv("BASE_PATH") or "").strip().strip("/")
    return f"/{raw}" if raw else ""
