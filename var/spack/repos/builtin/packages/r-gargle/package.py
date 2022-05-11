# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGargle(RPackage):
    """Utilities for Working with Google APIs.

    Provides utilities for working with Google APIs
    <https://developers.google.com/apis-explorer>. This includes functions and
    classes for handling common credential types and for preparing, executing,
    and processing HTTP requests."""

    cran = "gargle"

    version('1.2.0', sha256='4d46ca2933f19429ca5a2cfe47b4130a75c7cd9931c7758ade55bac0c091d73b')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-cli@3.0.0:', type=('build', 'run'))
    depends_on('r-fs@1.3.1:', type=('build', 'run'))
    depends_on('r-glue@1.3.0:', type=('build', 'run'))
    depends_on('r-httr@1.4.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('r-rlang@0.4.9:', type=('build', 'run'))
    depends_on('r-rstudioapi', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
