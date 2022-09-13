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
#     spack install libpressio-tthresh
#
# You can edit this file again by typing:
#
#     spack edit libpressio-tthresh
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class LibpressioTthresh(CMakePackage):
    """A tthresh implementation for libpressio"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/robertu94/libpressio_tthresh"
    url      = "https://github.com/robertu94/libpressio_tthresh/archive/refs/tags/0.0.1.tar.gz"
    git      = homepage

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['robertu94']

    version('main', branch="main")
    version('0.0.5', sha256='af47c90e9c16825312e390a7fb30d9d128847afb69ad6c2f6608bd80f60bae23')
    version('0.0.3', sha256='b0b0a4876d3362deafc2bb326be33882132e3d1666e0c5f916fd6fad74a18688')
    version('0.0.1', sha256='9efcfa97a5a81e9c456f50b712adb806d9d2f2ed6039860615df0f2e9d96569e')

    # FIXME: Add dependencies if required.
    depends_on('eigen')
    depends_on('libpressio@0.85.0:')

    def cmake_args(self):
        args = []
        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")
        return args

    
    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test(self):
        make('test')

