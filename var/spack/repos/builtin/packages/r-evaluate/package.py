# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REvaluate(RPackage):
    """Parsing and evaluation tools that make it easy to recreate the command
    line behaviour of R."""

    homepage = "https://cran.r-project.org/package=evaluate"
    url      = "https://cran.rstudio.com/src/contrib/evaluate_0.10.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/evaluate"

    version('0.10.1', '1dde5a35e2b9d57f1b1bb16791b35ff5')
    version('0.10', 'c49326babf984a8b36e7e276da370ad2')
    version('0.9',  '877d89ce8a9ef7f403b1089ca1021775')

    depends_on('r@3.0.2:')

    depends_on('r-stringr@0.6.2:', type=('build', 'run'))
