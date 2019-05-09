# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSnowfall(RPackage):
    """Usability wrapper around snow for easier development of parallel R
       programs. This package offers e.g. extended error checks, and additional
       functions. All functions work in sequential mode, too, if no cluster is
       present or wished. Package is also designed as connector to the cluster
       management tool sfCluster, but can also used without it."""

    homepage = "https://cran.r-project.org/web/packages/snowfall/index.html"
    url      = "https://cran.r-project.org/src/contrib/snowfall_1.84-6.1.tar.gz"

    version('1.84-6.1', '5ec38116aa9cac237d56f59ba5bd60e3')

    depends_on('r-snow', type=('build', 'run'))
