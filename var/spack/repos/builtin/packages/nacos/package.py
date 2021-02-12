# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nacos(MavenPackage):
    """Nacos is an easy-to-use platform designed for dynamic service
    discovery and configuration and service management. It helps you
    to build cloud native applications and microservices platform easily."""

    homepage = "https://nacos.io/"
    url      = "https://github.com/alibaba/nacos/archive/1.3.2.tar.gz"

    version('1.4.1', sha256='ac176a2497a503bf8420e0cdd26660fa734ea1e2d23bd9a01eb38430cbb4d171')
    version('1.4.0', sha256='77fa61161c95fb156e56ca05665b4b6b90b0b15c5e92c68cdf5bda0c2078f13f')
    version('1.3.2', sha256='3d3fdbe4033a9861a26c807d319db7c93f15de6491ddda512f9e5e421c563734')
