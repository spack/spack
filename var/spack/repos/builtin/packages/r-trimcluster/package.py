# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTrimcluster(RPackage):
    """trimcluster: Cluster analysis with trimming"""

    homepage = "http://www.homepages.ucl.ac.uk/~ucakche"
    url      = "https://cran.r-project.org/src/contrib/trimcluster_0.1-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/trimcluster"

    version('0.1-2', '7617920e224bd18f5b87db38a3116ec2')

    depends_on('r@1.9.0:')
