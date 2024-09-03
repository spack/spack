# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdmisc(RPackage):
    """Adrian Dusa's Miscellaneous."""

    homepage = "https://cran.r-project.org/package=admisc"
    cran = "admisc"

    version("0.34", sha256="fdcf875e6440fd049a78171db2594d6d963c484eca9387f852c5c8b3208a5bdf")
    version("0.33", sha256="3911bea32326bfc2e19d4f47d05e8ad7260da36fa2ae0bfde03540195081dbaa")
    version("0.32", sha256="d38ed1a3dbf549dff6759dad58c13ff3f236dbaa89f6f595459793f3e0b065b7")
    version("0.31", sha256="db385081c93f9d21adf4b8a8710ae0125a8dd01a87530b5051a3299997e0f4ea")
    version("0.30", sha256="690c3fc8f24466438dd818d263e53f19f238310175731daac42c62f0bbc46205")

    depends_on("r@3.5:")
