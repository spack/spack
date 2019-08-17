# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BppSuite(CMakePackage):
    """BppSuite is a suite of ready-to-use programs for phylogenetic and
       sequence analysis."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/BppSuite"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bppsuite/bppsuite-2.2.0.tar.gz"

    version('2.2.0', 'd8b29ad7ccf5bd3a7beb701350c9e2a4')

    depends_on('cmake@2.6:', type='build')
    depends_on('texinfo', type='build')
    depends_on('bpp-core')
    depends_on('bpp-seq')
    depends_on('bpp-phyl')
