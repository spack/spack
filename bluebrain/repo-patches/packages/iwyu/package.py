from spack import *
from spack.pkg.builtin.iwyu import Iwyu as BuiltinIwyu


class Iwyu(BuiltinIwyu):
    __doc__ = BuiltinIwyu.__doc__

    version('0.17', sha256='eca7c04f8b416b6385ed00e33669a7fa4693cd26cb72b522cde558828eb0c665')

    depends_on('ncurses')
    depends_on('llvm+clang@13.0:13', when='@0.17')
