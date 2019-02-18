# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRsnns(RPackage):
    """The Stuttgart Neural Network Simulator (SNNS) is a library containing
    many standard implementations of neural networks. This package wraps the
    SNNS functionality to make it available from within R. Using the RSNNS
    low-level interface, all of the algorithmic functionality and flexibility
    of SNNS can be accessed. Furthermore, the package contains a convenient
    high-level interface, so that the most common neural network topologies
    and learning algorithms integrate seamlessly into R."""

    homepage = "http://sci2s.ugr.es/dicits/software/RSNNS"
    url      = "https://cran.r-project.org/src/contrib/RSNNS_0.4-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RSNNS"

    version('0.4-7', 'ade7736611c456effb5f72e0ce0a1e6f')

    depends_on('r-rcpp', type=('build', 'run'))
