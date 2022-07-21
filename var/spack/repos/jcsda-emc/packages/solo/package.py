# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Solo(PythonPackage):
    """General tools for Python programmers to be used in various
    Python projects at JCSDA."""

    homepage = "https://github.com/JCSDA/solo"
    git = "https://github.com/JCSDA/solo.git"
    url = "https://github.com/JCSDA/solo/archive/refs/tags/1.0.0.tar.gz"

    maintainers = ['climbfuji', 'ericlingerfelt']

    version('develop', branch='develop', no_cache=True)
    version('1.0.0', commit='4231f2f917225704cc53b5238a51853a1beeb9b0', preferred=True)

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
