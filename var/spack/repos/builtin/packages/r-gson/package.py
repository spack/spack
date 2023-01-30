# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGson(RPackage):
    """Base Class and Methods for 'gson' Format.

    Proposes a new file format ('gson') for storing gene set and related
    information, and provides read, write and other utilities to process this
    file format."""

    cran = "gson"

    version("0.0.9", sha256="f694765cd2872efb73dd7be66ef8e31395915f9b277f59e0891cff138777b118")

    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"))
