# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from spack import *


class Qrupdate(MakefilePackage):
    """qrupdate is a Fortran library for fast updates of QR and
    Cholesky decompositions."""

    homepage = "http://sourceforge.net/projects/qrupdate/"
    url      = "https://downloads.sourceforge.net/qrupdate/qrupdate-1.1.2.tar.gz"

    version('1.1.2', '6d073887c6e858c24aeda5b54c57a8c4')

    depends_on("blas")
    depends_on("lapack")

    def edit(self, spec, prefix):
        # BSD "install" does not understand GNU -D flag.
        # We will create the parent directory ourselves.
        makefile = FileFilter('src/Makefile')
        if (sys.platform == 'darwin'):
            makefile.filter('-D', '')
        return

    def install(self, spec, prefix):
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        # Build static and dynamic libraries
        make('lib', 'solib',
             'BLAS={0}'.format(lapack_blas.ld_flags),
             'LAPACK={0}'.format(lapack_blas.ld_flags))
        # "INSTALL" confuses "make install" on case-insensitive filesystems
        if os.path.isfile("INSTALL"):
            os.remove("INSTALL")
        # create lib folder:
        if (sys.platform == 'darwin'):
            mkdirp(prefix.lib)
        make("install", "PREFIX=%s" % prefix)

    @run_after('install')
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if (sys.platform == 'darwin'):
            fix_darwin_install_name(self.spec.prefix.lib)
