# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTrimcluster(RPackage):
    """trimcluster: Cluster analysis with trimming"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cloud.r-project.org/src/contrib/trimcluster_0.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/trimcluster"

    version('0.1-2.1', sha256='b64a872a6c2ad677dfeecc776c9fe5aff3e8bab6bc6a8c86957b5683fd5d2300')
    version('0.1-2', '7617920e224bd18f5b87db38a3116ec2')

    depends_on('r@1.9.0:', type=('build', 'run'))
