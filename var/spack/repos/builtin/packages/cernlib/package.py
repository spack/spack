# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install cernlib
#
# You can edit this file again by typing:
#
#     spack edit cernlib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Cernlib(CMakePackage):
    """CERN Library"""

    homepage = "https://cernlib.web.cern.ch"
    url = "https://cernlib.web.cern.ch/cernlib/download/2022_source/tar/cernlib-2022.11.08.0-free.tar.gz"

    maintainers = ["andriish"]

    version("2022.11.08.0-free", sha256="733d148415ef78012ff81f21922d3bf641be7514b0242348dd0200cf1b003e46")

    # FIXME: Add dependencies if required.
    depends_on("motif")
    depends_on("libx11")

    def cmake_args(self):
        args = []
        return args
