# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBlob(RPackage):
    """R's raw vector is useful for storing a single binary object.
    What if you want to put a vector of them in a data frame? The blob
    package provides the blob object, a list of raw vectors, suitable
    for use as a column in data frame."""

    homepage = "https://cran.rstudio.com/web/packages/blob/index.html"
    url      = "https://cran.rstudio.com/src/contrib/blob_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/blob"
    version('1.1.0', '1c729aca36fd5193d81b1cd5ed9d8a00')

    depends_on('r-tibble', type=('build', 'run'))
