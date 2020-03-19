# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install arrayfire
#
# You can edit this file again by typing:
#
#     spack edit arrayfire
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Arrayfire(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
#    url      = "https://github.com/arrayfire/arrayfire/archive/v3.7.0.tar.gz"
    git      = "https://github.com/arrayfire/arrayfire.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('master', submodules=True)

    variant('cuda', default=False)
    variant('opencl', default=False)

    # FIXME: Add dependencies if required.
    depends_on('boost')
    depends_on('fftw')
    depends_on('openblas')
    depends_on('cuda', when='+cuda')
    depends_on('opencl', when='+opencl')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
