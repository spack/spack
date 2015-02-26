# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install atlas
#
# You can always get back here to change things with:
#
#     spack edit atlas
#
# See the spack documentation for more information on building
# packages.
#
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

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        #os.mkdir('ATLAS-Build')
        #os.chdir('ATLAS-Build')
        with working_dir('ATLAS-Build', create=True):
            self.module.configure = Executable('../configure')
        # FIXME: Modify the configure line to suit your build system here.
            configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
            make()
            make('check')
            make('ptcheck')
            make('time')
            make("install")
