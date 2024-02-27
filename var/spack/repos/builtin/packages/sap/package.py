# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sap(AutotoolsPackage):
    """SAP: pairwise structure alignment using double-dynamic programming"""

    homepage = "https://github.com/mathbio-nimr-mrc-ac-uk/SAP"
    url = "https://github.com/mathbio-nimr-mrc-ac-uk/SAP/archive/refs/tags/v.1.1.3.tar.gz"

    license("GPL-3.0-only", checked_by="A-N-Other")

    version("1.1.3", sha256="1ee5025f8a900cd9d9c490f7038b98d80a619e3015f2dc97b869ea3033c459e0")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
