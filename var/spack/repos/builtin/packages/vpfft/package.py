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
from spack import *


class Vpfft(MakefilePackage):
    """Proxy Application. VPFFT is an implementation of a mesoscale
    micromechanical materials model. By solving the viscoplasticity
    model, VPFFT simulates the evolution of a material under deformation.
    The solution time to the viscoplasticity model, described by a set
    of partial differential equations, is significantly reduced by the
    application of Fast Fourier Transform in the VPFFT algorithm.
    """

    homepage = "http://www.exmatex.org/vpfft.html"
    git      = "https://github.com/exmatex/VPFFT.git"

    tag = ['proxy-app']

    version('develop')

    depends_on('eigen')
    depends_on('fftw')
    depends_on('mpi')

    @property
    def build_targets(self):
        targets = [
            "--file=Makefile.make",
            "EIGEN_PATH={0}".format(
                join_path(
                    self.spec['eigen'].prefix.include,
                    'eigen{0}'.format(
                        self.spec['eigen'].version.up_to(1)))),
            "FFTW_PATH={0}".format(self.spec['fftw'].prefix),
            "CC={0}".format(self.spec['mpi'].mpicxx)
        ]
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('VPFFT++', prefix.bin)
        install('README.md', prefix)
        install('README.make', prefix)
        install('README-license.txt', prefix)
        install_tree('docs', prefix.docs)
