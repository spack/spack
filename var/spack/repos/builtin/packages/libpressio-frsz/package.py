# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install libpressio-frsz
#
# You can edit this file again by typing:
#
#     spack edit libpressio-frsz
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------


class LibpressioFrsz(CMakePackage):
    """Fized Rate SZ"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/robertu94/frsz"
    url = "https://github.com/robertu94/frsz"
    git = "ssh://git@github.com/robertu94/frsz"

    maintainers = ["robertu94"]

    version("master", branch="main")

    depends_on("libpressio")

    def cmake_args(self):
        args = ["-DBUILD_TESTING=OFF"]
        return args
