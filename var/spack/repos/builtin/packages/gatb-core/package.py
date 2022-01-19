# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GatbCore(CMakePackage):
    """GATB - The Genome Analysis Toolbox with de-Bruijn graph"""

    homepage = "https://gatb.inria.fr/software/gatb-core/"
    git      = "https://github.com/GATB/gatb-core.git"

    depends_on('cmake@3.1.0:', type='build')

    version('1.4.2', tag='v1.4.2')
    version('1.4.1', tag='v1.4.1')

    root_cmakelists_dir = 'gatb-core'
