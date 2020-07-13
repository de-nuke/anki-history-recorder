import re
import unicodedata

from aqt import mw


def strip_accents(s: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalize_to_filename(value: str) -> str:
    """
    Convert spaces to hyphens. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace.
    """
    value = strip_accents(value)\
        .encode('ASCII', 'replace')\
        .decode('ascii')\
        .replace('?', '_')
    value = re.sub(r'[^\w\s-]', '_', value).strip()
    return re.sub(r'[-\s]+', '_', value)


def get_config() -> dict:
    if getattr(getattr(mw, "addonManager", None), "getConfig", None):
        config = mw.addonManager.getConfig(__name__) or {}
    else:
        config = {
            "region": "eu",
            "enabled-by-default": True,
            "live-sync": True,
            "display-status": True
        }
    return config
