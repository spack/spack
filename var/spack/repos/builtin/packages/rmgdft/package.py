# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rmgdft(CMakePackage):
    """RMG is an Open Source code for electronic structure calculations and
    modeling of materials and molecules. It is based on density functional
    theory and uses a real space basis and pseudopotentials.i
    """

    homepage = "http://www.rmgdft.org/"
    url      = "https://github.com/RMGDFT/rmgdft/archive/v4.0.0-beta.3.tar.gz"

    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('4.0.0-beta.3', 'b827762e2da539bf2d41ec5512a7d900')

#    Have not gotten this to work correctly yet.
#    variant('rmg-cuda', default=False,
#    description='Base version of the code using cuda')

    # openmpi, mpich etc
    depends_on('mpi')

    # 1.61 is not the most recent release but newer versions seem to have some
    # issues with cmake.
    depends_on('boost@1.61.0%gcc +shared')

    depends_on('fftw')

    # To get good performance some tweaking of this will be required
    # on most systems
    depends_on('blas')

    # Needed for qmcpack integration
    # depends_on('hdf5')
    depends_on('hdf5@1.8.16:+hl~mpi')

    def cmake_args(self):
        args = ['-DBoost_USE_STATIC_LIBS=OFF']
        return args
