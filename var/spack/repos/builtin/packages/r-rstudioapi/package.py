# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRstudioapi(RPackage):
    """Access the RStudio API (if available) and provide informative error
    messages when it's not."""

    homepage = "https://cloud.r-project.org/package=rstudioapi"
    url      = "https://cloud.r-project.org/src/contrib/rstudioapi_0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rstudioapi"

    version('0.10', sha256='80c5aa3063bcab649904cb92f0b164edffa2f6b0e6a8f7ea28ae317b80e1ab96')
    version('0.9.0', sha256='5149a2830ae7134c396ce64764b263cf9f348d4399f53da3804f40d7d5bec13e')
    version('0.7', 'ee4ab567a7a9fdfac1a6fd01fe38de4a')
    version('0.6', 'fdb13bf46aab02421557e713fceab66b')
    version('0.5', '6ce1191da74e7bcbf06b61339486b3ba')
