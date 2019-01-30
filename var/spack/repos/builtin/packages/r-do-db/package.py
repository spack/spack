# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDoDb(RPackage):
    """A set of annotation maps describing the entire Disease
    Ontology assembled using data from DO."""

    homepage = "https://bioconductor.org/packages/DO.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/DO.db_2.9.tar.gz"

    version('2.9', '63dda6d46d2fe40c52a2e79260a7fb9d')

    depends_on('r-annotationdbi', type=('build', 'run'))
