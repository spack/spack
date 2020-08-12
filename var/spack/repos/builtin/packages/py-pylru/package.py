# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPylru(PythonPackage):
    """A least recently used (LRU) cache implementation"""

    homepage = "https://github.com/jlhutch/pylru"
    url = "https://pypi.io/packages/source/p/pylru/pylru-1.1.0.tar.gz"

    depends_on('py-setuptools', type=('build', 'run'))

    version('1.2.0', sha256='492f934bb98dc6c8b2370c02c95c65516ddc08c8f64d27f70087eb038621d297')
    version('1.1.0', sha256='e03a3d354eb8fdfa11638698e8a1f06cd3b3a214ebc0a120c603a79290d9ebec')
