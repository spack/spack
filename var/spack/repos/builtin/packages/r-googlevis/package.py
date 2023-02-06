# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGooglevis(RPackage):
    """R Interface to Google Charts.

    R interface to Google Charts API, allowing users to create interactive
    charts based on data frames. Charts are displayed locally via the R HTTP
    help server. A modern browser with an Internet connection is required and
    for some charts a Flash player. The data remains local and is not uploaded
    to Google."""

    cran = "googleVis"

    version("0.7.0", sha256="5f1636024e678f9973e3ce605b46f46ea9cdffd58b98e315b495e66f34eb02e9")
    version("0.6.11", sha256="f8c90b6c51da7bf184bff6762d98fc24faba1b634724ecdb987161ee10987b97")
    version("0.6.9", sha256="0739d0a3382a73a824b5ff9a6fe329198dd05c9da5855ac051ed022d7b41b7ea")
    version("0.6.4", sha256="7dcaf0e9d5e5598c17e8bd474141708de37eeb2578b09788431b9d871edb7eb8")
    version("0.6.3", sha256="17d104c5d4e6ab7b984df229cd51be19681e4726077afec7c61a33f6e4c0b6ef")
    version("0.6.0", sha256="862708097fbb5d4e83193777f40979d7848f9841d94d48ee8a74106266acc440")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
