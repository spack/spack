##############################################################################
# Copyright (c) 2013-2020, Lawrence Livermore National Security, LLC.
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


class AsdfCxx(CMakePackage):
    """ASDF - Advanced Scientific Data Format, a C++ implementation"""

    homepage = "https://github.com/eschnett/asdf-cxx"
    url      = "https://github.com/eschnett/asdf-cxx/archive/version/1.0.0.tar.gz"

    version('7.2.1', sha256='40864f4f27d3ce8acb5169b57211ce6ac3805f0a6de9c1dfd5f994f4a5beccda')
    version('7.2.0', sha256='faded85d44288afb83f13634d2139adee07e06f7ea60960c6f2ef8d898c0aa09')
    version('7.1.0', sha256='81fd8c7f91f8daf0f85a1486480ae9e736b9712e82ccb858271f7ee2c2b425f7')
    version('7.0.0', sha256='a50718dfa68b86b0c3e280e6a9d0a4edb03d500ba70244bd38fa86bac1433979')
    version('6.3.0', '5f7a24a62b398991b38abbfb14f3eb67')
    version('6.0.0', '8881646c4a3cca88e733adcdd6e03070')
    version('5.0.0', '0dfe3641ec0776de28715d0509f48210')
    version('4.0.1', '04e0a5bf834343920f2671d8ce6bdaf5')
    version('3.1.0', '02355a034ffbb97404db8f0ce88b8107')
    version('3.0.0', 'ae8af474c3ea890ce7bb9cfdf609f429')
    version('2.6.1', '071d2a2a0348e7fce3a72ab5f5b249ed')
    version('2.5.1', '0b17ea36681acc4959412f55ce8e8308')
    version('2.5.0', '9d2c28b8b62cc1f5d3aadbebe43c8767')
    version('2.4.1', '68e50c7597c79e47e311df5b37960439')
    version('2.4.0', 'ebce6859db74c91c2e11422052078a49')
    version('2.3.1', 'dd3bf93d05b189b5486aa94b5abc2028')
    version('2.2.1', '20df71ea7e9cbcdf4a9f8495b3005cd1')
    version('2.1.1', '203acdd49ba7133e69b6a29de95910ad')
    version('2.1.0', '9baf440e85dc00bea9cb3f77ca7c4d0a')
    version('1.1.0', 'd054a51d89c212879b6c9869f6a2c85c')
    version('1.0.0', 'c2353a3705615ed47c2c0871dca0a272')

    variant('python', default=True, description="Enable Python support")

    depends_on('bzip2')
    depends_on('openssl')
    depends_on('py-numpy', type=('build', 'run'), when='+python')
    depends_on('python', type=('build', 'run'), when='+python')
    depends_on('swig', type='build', when='+python')
    depends_on('yaml-cpp')
    depends_on('zlib')

    def cmake_args(self):
        args = []
        return args
