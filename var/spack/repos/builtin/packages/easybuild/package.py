# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Easybuild(PythonPackage):
    """EasyBuild is a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild/easybuild-3.1.2.tar.gz'

    version('3.1.2', 'c2d901c2a71f51b24890fa69c3a46383')

    depends_on('py-easybuild-framework@3.1.2', when='@3.1.2', type='run')
    depends_on('py-easybuild-easyblocks@3.1.2', when='@3.1.2', type='run')
    depends_on('py-easybuild-easyconfigs@3.1.2', when='@3.1.2', type='run')
