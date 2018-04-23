##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
