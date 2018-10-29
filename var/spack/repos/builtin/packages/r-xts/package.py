# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXts(RPackage):
    """Provide for uniform handling of R's different time-based data classes by
    extending zoo, maximizing native format information preservation and
    allowing for user level customization and extension, while simplifying
    cross-class interoperability."""

    homepage = "http://r-forge.r-project.org/projects/xts/"
    url      = "https://cran.r-project.org/src/contrib/xts_0.9-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/xts"

    version('0.9-7', 'a232e94aebfa654653a7d88a0503537b')

    depends_on('r-zoo', type=('build', 'run'))
