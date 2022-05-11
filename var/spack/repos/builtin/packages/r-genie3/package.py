# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGenie3(RPackage):
    """GEne Network Inference with Ensemble of trees.

       This package implements the GENIE3 algorithm for inferring gene
       regulatory networks from expression data."""

    bioc = "GENIE3"

    version('1.16.0', commit='5543b1b883d3a1c92e955de6668444278edc2bdf')
    version('1.12.0', commit='14289cee9bed113ab35ba03bcaac4a30e5784497')
    version('1.6.0', commit='d6a49182e098342afe77f01c322dfc7b72450502')
    version('1.4.3', commit='ae719c759f23f09d28fcf1acc45b860cd7761f08')
    version('1.2.1', commit='1b56fe8184d521d1bb247f000efe9e2b540604c9')
    version('1.0.0', commit='eb7c95ed12ea50d61e8fa20bc2b25ae9d74c302f')

    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'), when='@1.16.0:')
