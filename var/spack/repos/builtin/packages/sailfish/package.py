# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sailfish(CMakePackage):
    """Sailfish is a tool for transcript quantification from RNA-seq data."""

    homepage = "http://www.cs.cmu.edu/~ckingsf/software/sailfish"
    url      = "https://github.com/kingsfordgroup/sailfish/archive/v0.10.1.tar.gz"

    version('0.10.1', 'e6dab4cf3a39f346df7c28f40eb58cad')

    depends_on('boost@1.55:')
    depends_on('tbb')
