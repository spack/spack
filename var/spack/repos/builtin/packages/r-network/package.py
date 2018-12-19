# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNetwork(RPackage):
    """Tools to create and modify network objects. The network class can
       represent a range of relational data types, and supports
       arbitrary vertex/edge/graph attributes."""

    homepage = "https://statnet.org"
    url      = "https://cran.r-project.org/src/contrib/network_1.13.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/network"

    version('1.13.0', 'd0b967d6f1aad43b6479d72f29b705de')
