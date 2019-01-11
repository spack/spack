# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TrnascanSe(AutotoolsPackage):
    """Seaching for tRNA genes in genomic sequence"""

    homepage = "http://lowelab.ucsc.edu/tRNAscan-SE/"
    url      = "http://trna.ucsc.edu/software/trnascan-se-2.0.0.tar.gz"

    version('2.0.0',    '36d2b53bcb281efbae09e0305346e544')
