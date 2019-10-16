# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TrnascanSe(AutotoolsPackage):
    """Seaching for tRNA genes in genomic sequence"""

    homepage = "http://lowelab.ucsc.edu/tRNAscan-SE/"
    url      = "http://trna.ucsc.edu/software/trnascan-se-2.0.0.tar.gz"

    version('2.0.0',    sha256='0dde1c07142e4bf77b21d53ddf3eeb1ef8c52248005a42323d13f8d7c798100c')
