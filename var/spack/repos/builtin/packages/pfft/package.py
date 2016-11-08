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


class Pfft(AutotoolsPackage):
    """PFFT is a software library for computing massively parallel,
       fast Fourier transformations on distributed memory architectures.
       PFFT can be understood as a generalization of FFTW-MPI to
       multidimensional data decomposition."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software.php.en"
    url      = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software/pfft-1.0.8-alpha.tar.gz"

    version('1.0.8-alpha', '46457fbe8e38d02ff87d439b63dc0709')

    depends_on('fftw+mpi+pfft_patches')
    depends_on('mpi')

    def install(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        configure(*options)
        make()
        if self.run_tests:
            make("check")
        make("install")

        if '+float' in spec['fftw']:
            configure('--enable-float', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
        if '+long_double' in spec['fftw']:
            configure('--enable-long-double', *options)
            make()
            if self.run_tests:
                make("check")
            make("install")
