from spack import *
from spack.util.executable import Executable
import os

class Atlas(Package):
    """
    Automatically Tuned Linear Algebra Software, generic shared
    ATLAS is an approach for the automatic generation and optimization of
    numerical software. Currently ATLAS supplies optimized versions for the
    complete set of linear algebra kernels known as the Basic Linear Algebra
    Subroutines (BLAS), and a subset of the linear algebra routines in the
    LAPACK library.
    """
    homepage = "http://math-atlas.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/math-atlas/Stable/3.10.2/atlas3.10.2.tar.bz2"

    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da')

    def install(self, spec, prefix):
        with working_dir('ATLAS-Build', create=True):
            self.module.configure = Executable('../configure')
            configure("--prefix=%s" % prefix)

            make()
            make('check')
            make('ptcheck')
            make('time')
            make("install")
