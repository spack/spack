# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildEasyblocks(PythonPackage):
    """Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = 'http://hpcugent.github.io/easybuild/'
    url      = 'https://pypi.io/packages/source/e/easybuild-easyblocks/easybuild-easyblocks-3.1.2.tar.gz'

    version('3.1.2', 'be08da30c07e67ed3e136e8d38905fbc')

    depends_on('py-easybuild-framework@3.1:', when='@3.1:', type='run')
