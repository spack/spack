from spack import *

import os
from llnl.util.filesystem import join_path

class Tau(Package):
    """A portable profiling and tracing toolkit for performance
       analysis of parallel programs written in Fortran, C, C++, UPC,
       Java, Python."""
    homepage = "http://www.cs.uoregon.edu/research/tau"
    url      = "http://www.cs.uoregon.edu/research/paracomp/tau/tauprofile/dist/tau-2.23.1.tar.gz"

    version('2.23.1', '6593b47ae1e7a838e632652f0426fe72')
    version('2.23-perfdb', 'c97b404bcd94c7d9b04fa3dc0a32b0d1',
            url='http://www.nic.uoregon.edu/~khuck/tau2-latest.tar.gz')

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.
        change_sed_delimiter('@', ';', 'configure')
        change_sed_delimiter('@', ';', 'utils/FixMakefile')
        change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')

        # After that, it's relatively standard.
        configure("-prefix=%s" % prefix)
        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()


    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ('bin', 'lib'):
                src  = join_path(self.prefix, subdir, d)
                dest = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dest):
                    os.symlink(join_path(subdir, d), dest)
