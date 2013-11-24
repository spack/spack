from itertools import product
from spack.util.executable import which

# Supported archvie extensions.
PRE_EXTS = ["tar"]
EXTS     = ["gz", "bz2", "xz", "Z", "zip", "tgz"]

# Add EXTS last so that .tar.gz is matched *before* tar.gz
ALLOWED_ARCHIVE_TYPES = [".".join(l) for l in product(PRE_EXTS, EXTS)] + EXTS


def decompressor_for(path):
    """Get the appropriate decompressor for a path."""
    tar = which('tar', required=True)
    tar.add_default_arg('-xf')
    return tar
