# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CodarCheetah(Package):
    """CODAR Cheetah:
    The CODAR Experiment Harness for Exascale science applications.
    """

    homepage = "https://github.com/CODARcode/cheetah"
    url      = "https://github.com/CODARcode/cheetah/archive/v0.1.tar.gz"
    git      = "https://github.com/CODARcode/cheetah.git"

    version('develop', branch='master')
    version('0.1', '6918021f74fa7a2f1de26c0bb31a63ef')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('savanna')

    def install(self, spec, prefix):
        install_tree('.', prefix)
