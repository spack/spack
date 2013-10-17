#
# This needs to be expanded for full compiler support.
#

import spack
import spack.compilers.gcc
from spack.util.lang import memoized, list_modules

@memoized
def supported_compilers():
    return [c for c in list_modules(spack.compilers_path)]


@memoized
def default_compiler():
    from spack.spec import Compiler
    return Compiler('gcc', gcc.get_version())
