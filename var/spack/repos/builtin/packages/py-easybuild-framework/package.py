# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildFramework(PythonPackage):
    """The core of EasyBuild, a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild-framework/easybuild-framework-3.1.2.tar.gz'

    version('3.1.2', '283bc5f6bdcb90016b32986d52fd04a8')

    depends_on('python@2.6:2.8', type='run')
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-vsc-base@2.5.4:', when='@2.9:', type='run')
    depends_on('py-vsc-install', type='run')  # only required for tests (python -O -m test.framework.suite)
