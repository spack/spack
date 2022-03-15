# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRbibutils(RPackage):
    """Convert Between Bibliography Formats.

    Converts between a number of bibliography formats, including 'BibTeX',
    'BibLaTeX' and 'Bibentry'. Includes a port of the 'bibutils' utilities by
    Chris Putnam <https://sourceforge.net/projects/bibutils/>. Supports all
    bibliography formats and character encodings implemented in 'bibutils'."""

    cran = "rbibutils"

    version('2.2.7', sha256='7c9e6719556b8caa9fb58743b717e89f45e8e7018371bf16f07dc3c1f96a55c5')
    version('2.0', sha256='03d13abee321decb88bc4e7c9f27276d62a4a880fa72bb6b86be91885010cfed')

    depends_on('r@2.10:', type=('build', 'run'))
