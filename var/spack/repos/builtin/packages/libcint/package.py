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


class Libcint(CMakePackage):
    """Library for analytical Gaussian integrals for quantum chemistry."""

    homepage    = "https://github.com/sunqm/libcint"
    url         = "https://github.com/sunqm/libcint/archive/v3.0.4.tar.gz"
    maintainers = ['mfherbst']

    #
    # Versions
    #
    version('3.0.12', 'e69117782ff9f443373f30c80ecb6ab7')
    version('3.0.11', '1fb1db5a426280d38cddbb0098f6c678')
    version('3.0.10', 'b368e257dba99febf1cdd1391f2e58a3')
    version('3.0.8',  '61f415ad9c7854963136c6bba7a661eb')
    version('3.0.7',  'f0f3c971c0d5bb5565ac9ab5e271aa79')
    version('3.0.6',  '1aafd91107e2418f794ce02b9d88ea8b')
    version('3.0.5',  'facb1ddabd9497e99d22176a9b9a895f')
    version('3.0.4',  '55607a61313225ef4434d3e96624a008')

    #
    # Variants
    #
    variant('f12', default=True,
            description="Enable explicitly correlated f12 integrals.")
    variant('coulomb_erf', default=True,
            description="Enable attenuated coulomb operator integrals.")
    variant('test', default=False, description="Build test programs")
    variant('shared', default=True,
            description="Build the shared library")

    #
    # Dependencies and conflicts
    #
    depends_on('cmake@2.6:', type="build")
    depends_on('blas')
    depends_on('python', type=("build", "test"), when="+test")
    depends_on('py-numpy', type=("build", "test"), when="+test")

    # Libcint tests only work with a shared libcint library
    conflicts('+test~shared')

    #
    # Settings and cmake cache
    #
    def cmake_args(self):
        spec = self.spec
        args = [
            "-DWITH_COULOMB_ERF=" + str("+coulomb_erf" in spec),
            "-DWITH_F12=" + str("+f12" in spec),
            "-DBUILD_SHARED_LIBS=" + str("+shared" in spec),
            "-DENABLE_TEST=" + str("+test" in spec),
            "-DENABLE_EXAMPLE=OFF",  # Requires fortran compiler
        ]
        return args
