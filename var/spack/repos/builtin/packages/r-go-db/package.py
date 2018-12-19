# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGoDb(RPackage):
    """A set of annotation maps describing the entire Gene
    Ontology assembled using data from GO."""

    homepage = "https://www.bioconductor.org/packages/GO.db/"
    url = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/GO.db_3.4.1.tar.gz"

    version('3.4.1', 'e16ee8921d8adc1ed3cbac2a3e35e386')
    depends_on('r-annotationdbi', type=('build', 'run'))
