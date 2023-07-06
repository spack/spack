# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RListenv(RPackage):
    """Environments Behaving (Almost) as Lists.

    List environments are environments that have list-like properties. For
    instance, the elements of a list environment are ordered and can be
    accessed and iterated over using index subsetting."""

    cran = "listenv"

    version("0.9.0", sha256="352841e04f0725d361b78cfdc75e00511f740d97237dd651ea86aa5484674887")
    version("0.8.0", sha256="fd2aaf3ff2d8d546ce33d1cb38e68401613975117c1f9eb98a7b41facf5c485f")
    version("0.7.0", sha256="6126020b111870baea08b36afa82777cd578e88c17db5435cd137f11b3964555")

    depends_on("r@3.1.2:", type=("build", "run"))
