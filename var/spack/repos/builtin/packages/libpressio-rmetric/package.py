# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install libpressio-rmetric
#
# You can edit this file again by typing:
#
#     spack edit libpressio-rmetric
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class LibpressioRmetric(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/robertu94/libpressio-rmetric/archive/refs/tags/0.0.2.tar.gz"
    git      = "https://github.com/robertu94/libpressio-rmetric"

    maintainers = ['robertu94']

    version('master', branch='master')
    #note versions <= 0.0.3 do not build with spack
    version('0.0.4', sha256='166af5e84d7156c828a3f0dcc5bf531793ea4ec44bbf468184fbab96e1f0a91f')
    version('0.0.3', sha256='c45948f83854c87748c7ec828ca2f06d7cf6f98a34f763b68c13a4e2deb7fd79')

    depends_on('libpressio@0.85.0:')
    depends_on('r')
    depends_on('r-rcpp')
    depends_on('r-rinside')

    def cmake_args(self):
        args = ['HAS_SPACK=ON']

        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")

        return args

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test(self):
        make('test')
