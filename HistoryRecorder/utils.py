import re
import unicodedata


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
)


def normalize_to_filename(value):
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
