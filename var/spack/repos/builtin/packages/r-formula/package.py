# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RFormula(RPackage):
    """Infrastructure for extended formulas with multiple parts on the right-hand
    side and/or multiple responses on the left-hand side."""

    homepage = "https://cloud.r-project.org/package=Formula"
    url      = "https://cloud.r-project.org/src/contrib/Formula_1.2-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Formula"

    version('1.2-3', sha256='1411349b20bd09611a9fd0ee6d15f780c758ad2b0e490e908facb49433823872')
    version('1.2-2', 'c69bb0522811cf8eb9f1cc6c3d182b6e')
    version('1.2-1', '2afb31e637cecd0c1106317aca1e4849')

    depends_on('r@2.0.0:', type=('build', 'run'))
