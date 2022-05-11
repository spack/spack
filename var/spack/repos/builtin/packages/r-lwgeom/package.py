# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RLwgeom(RPackage):
    """Bindings to Selected 'liblwgeom' Functions for Simple Features.

    Access to selected functions found in 'liblwgeom'
    <https://github.com/postgis/postgis/tree/master/liblwgeom>, the
    light-weight geometry library used by 'PostGIS' <https://postgis.net/>."""

    cran = "lwgeom"

    version('0.2-8', sha256='f48a92de222da0590b37a30d5cbf2364555044a842795f6b488afecc650b8b34')
    version('0.2-5', sha256='4a1d93f96c10c2aac173d8186cf7d7bef7febcb3cf066a7f45da32251496d02f')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-units', type=('build', 'run'))
    depends_on('r-sf@0.9-3:', type=('build', 'run'))
    depends_on('geos@3.5.0:')
    depends_on('proj@4.8.0:6.999')
    depends_on('sqlite', when='@0.2-8:')
