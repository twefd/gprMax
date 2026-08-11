"""Thin wrapper around ``streamlit-image-coordinates`` for click-to-place.

The published component (0.4.0) does ``from streamlit.elements.image import
UseColumnWith`` at import time. Newer Streamlit removed that symbol, but the
component only uses it in a *stringised* type annotation (its module has
``from __future__ import annotations``), so it is never actually evaluated.
We inject a harmless placeholder so the import succeeds on current Streamlit.

Exposes:
    AVAILABLE            – True if the component imported successfully
    image_coordinates()  – the component function (or None if unavailable)
"""

from __future__ import annotations

import streamlit.elements.image as _st_image

# Provide the name the old component expects, if the running Streamlit lacks it.
if not hasattr(_st_image, "UseColumnWith"):
    _st_image.UseColumnWith = str  # only referenced in a stringised annotation

try:
    from streamlit_image_coordinates import streamlit_image_coordinates as _imgc
    AVAILABLE = True
except Exception:  # noqa: BLE001 - degrade gracefully to the static preview
    _imgc = None
    AVAILABLE = False


def image_coordinates(*args, **kwargs):
    """Call the underlying component; raises if it could not be imported."""
    if _imgc is None:
        raise RuntimeError("streamlit-image-coordinates is not available")
    return _imgc(*args, **kwargs)
