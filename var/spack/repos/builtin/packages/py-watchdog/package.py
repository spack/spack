# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWatchdog(PythonPackage):
    """Python library and shell utilities to monitor filesystem events."""

    homepage = "https://github.com/gorakhargosh/watchdog"
    pypi     = "watchdog/watchdog-0.10.3.tar.gz"

    version('2.1.6',  sha256='a36e75df6c767cbf46f61a91c70b3ba71811dfa0aca4a324d9407a06a8b7a2e7')
    version('0.10.3', sha256='4214e1379d128b0588021880ccaf40317ee156d4603ac388b9adcf29165e0c04')

    variant('watchmedo', default=False, description="Build optional watchmedo utility script")

    depends_on('python@2.7,3.4:',     type=('build', 'run'))
    depends_on('python@3.6:',         type=('build', 'run'), when='@2.1.6:')
    depends_on('py-setuptools',       type='build')
    depends_on('py-pathtools@0.1.1:', type=('build', 'run'), when='@0.10.3')
    depends_on('py-pyyaml@3.10:',     type=('build', 'run'), when='+watchmedo')
    depends_on('py-argh@0.24.1:',     type=('build', 'run'), when='@0.10.3+watchmedo')
