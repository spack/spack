# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install calculix
#
# You can edit this file again by typing:
#
#     spack edit calculix
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Calculix(Package):
    """CalculiX : A Free Software Three-Dimensional Structural Finite Element Program"""

    homepage = "https://www.dhondt.de"
    url = "https://www.dhondt.de/cgx_2.21.all.tar.bz2"
    license("GPL-2.0-only", checked_by="catalinbostan")
    version("2.21", sha256="55ae561903df011e944d7f82f9e00039dbc4c68ac9195a5a862d446eb56bcfc1")

    def install(self, spec, prefix):
        with working_dir("CalculiX/cgx_2.21/src"):
            make()
            mkdir(prefix.bin)
            install("cgx", prefix.bin)
