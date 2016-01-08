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

    version('3.11.34', '0b6c5389c095c4c8785fd0f724ec6825',
            url='http://sourceforge.net/projects/math-atlas/files/Developer%20%28unstable%29/3.11.34/atlas3.11.34.tar.bz2/download')
    version('3.10.2', 'a4e21f343dec8f22e7415e339f09f6da',
            url='http://downloads.sourceforge.net/project/math-atlas/Stable/3.10.2/atlas3.10.2.tar.bz2')

    # TODO: make this provide BLAS once it works better.  Create a way
    # TODO: to mark "beta" packages and require explicit invocation.

    # provides('blas')


    def patch(self):
        # Disable thraed check.  LLNL's environment does not allow
        # disabling of CPU throttling in a way that ATLAS actually
        # understands.
        filter_file(r'^\s+if \(thrchk\) exit\(1\);', 'if (0) exit(1);',
                    'CONFIG/src/config.c')
        # TODO: investigate a better way to add the check back in
        # TODO: using, say, MSRs.  Or move this to a variant.

    @when('@:3.10')
    def install(self, spec, prefix):
        with working_dir('ATLAS-Build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, '-C', 'ic', 'cc', '-C', 'if', 'f77', "--dylibs")
            make()
            make('check')
            make('ptcheck')
            make('time')
            make("install")


    def install(self, spec, prefix):
        with working_dir('ATLAS-Build', create=True):
            configure = Executable('../configure')
            configure('--incdir=%s' % prefix.include,
                      '--libdir=%s' % prefix.lib,
                      '--cc=cc',
                      "--shared")

            make()
            make('check')
            make('ptcheck')
            make('time')
            make("install")
