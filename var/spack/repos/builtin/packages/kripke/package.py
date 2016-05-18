##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from spack import *

class Kripke(Package):
    """Kripke is a simple, scalable, 3D Sn deterministic particle
       transport proxy/mini app.
    """
    homepage = "https://codesign.llnl.gov/kripke.php"
    url      = "https://codesign.llnl.gov/downloads/kripke-openmp-1.1.tar.gz"

    version('1.1', '7fe6f2b26ed983a6ce5495ab701f85bf')

    variant('mpi',    default=True, description='Build with MPI.')
    variant('openmp', default=True, description='Build with OpenMP enabled.')

    depends_on('mpi', when="+mpi")

    def install(self, spec, prefix):
        with working_dir('build', create=True):
            def enabled(variant):
                return (1 if variant in spec else 0)

            cmake('-DCMAKE_INSTALL_PREFIX:PATH=.',
                  '-DENABLE_OPENMP=%d' % enabled('+openmp'),
                  '-DENABLE_MPI=%d' % enabled('+mpi'),
                  '..',
                  *std_cmake_args)
            make()

            # Kripke does not provide install target, so we have to copy
            # things into place.
            mkdirp(prefix.bin)
            install('kripke', prefix.bin)
