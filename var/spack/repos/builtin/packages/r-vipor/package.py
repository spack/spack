# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVipor(RPackage):
    """Plot Categorical Data Using Quasirandom Noise and Density Estimates"""

    homepage = "https://cloud.r-project.org/package=vipor"
    url      = "https://cloud.r-project.org/src/contrib/vipor_0.4.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vipor"

    version('0.4.5', 'd08bc95b3aaf1574bf41b7eb41b67ce4')
    version('0.4.4', '834212e3971787809ba9737744d54dee')

    depends_on('r@3.0.0:', type=('build', 'run'))
