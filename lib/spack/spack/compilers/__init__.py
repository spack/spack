#
# This needs to be expanded for full compiler support.
#

import spack
import spack.compilers.gcc
from spack.util import list_modules, memoized


@memoized
def supported_compilers():
    return [c for c in list_modules(spack.compilers_path)]


def get_compiler():
    return Compiler('gcc', spack.compilers.gcc.get_version())
