# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RHexbin(RPackage):
    """Binning and plotting functions for hexagonal bins. Now uses and relies
    on grid graphics and formal (S4) classes and methods."""

    homepage = "http://github.com/edzer/hexbin"
    url      = "https://cran.r-project.org/src/contrib/hexbin_1.27.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/hexbin"

    version('1.27.2', sha256='46d47b1efef75d6f126af686a4dd614228b60418b9a5bde9e9e5d11200a0ee52')
    version('1.27.1', '7590ed158f8a57a71901bf6ca26f81be')

    depends_on('r-lattice', type=('build', 'run'))
