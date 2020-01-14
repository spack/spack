# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CodarCheetah(PythonPackage):
    """CODAR Cheetah:
    The CODAR Experiment Harness for Exascale science applications.
    """

    maintainers = ['kshitij-v-mehta']

    homepage = "https://github.com/CODARcode/cheetah"
    url      = "https://github.com/CODARcode/cheetah/archive/v0.1.tar.gz"
    git      = "https://github.com/CODARcode/cheetah.git"

    version('develop', branch='dev')
    version('0.5', sha256='f37a554741eff4bb8407a68f799dd042dfc4df525e84896cad70fccbd6aca6ee')

    depends_on('python@3.5:', type=('build', 'run'))
