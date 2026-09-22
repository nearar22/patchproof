"""Work around Windows refusing to unlink the direct VM temporary file."""
import os
_unlink = os.unlink
def _safe(path, *args, **kwargs):
    try: return _unlink(path, *args, **kwargs)
    except PermissionError: return None
os.unlink = _safe

