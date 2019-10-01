# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rmgdft
#
# You can edit this file again by typing:
#
#     spack edit rmgdft
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------


from spack import *


class Rmgdft(CMakePackage):
    """RMG is an Open Source code for electronic structure calculations and
    modeling of materials and molecules. It is based on density functional
    theory and uses a real space basis and pseudopotentials.i
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.rmgdft.org/"
    url      = "https://github.com/RMGDFT/rmgdft/archive/v4.0.0-beta.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
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
