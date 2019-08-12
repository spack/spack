# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildEasyconfigs(PythonPackage):
    """Collection of easyconfig files for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild-easyconfigs/easybuild-easyconfigs-3.1.2.tar.gz'

    version('3.1.2', '13a4a97fe8a5b9a94f885661cf497d13')

    depends_on('py-easybuild-framework@3.1:', when='@3.1:', type='run')
    depends_on('py-easybuild-easyblocks@3.1.2:', when='@3.1.2', type='run')
