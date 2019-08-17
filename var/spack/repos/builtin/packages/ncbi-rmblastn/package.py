# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NcbiRmblastn(AutotoolsPackage):
    """RMBlast search engine for NCBI"""

    homepage = "https://www.ncbi.nlm.nih.gov/"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/rmblast/LATEST/ncbi-rmblastn-2.2.28-src.tar.gz"

    version('2.2.28', 'fb5f4e2e02ffcb1b17af2e9f206c5c22')

    configure_directory = 'c++'
