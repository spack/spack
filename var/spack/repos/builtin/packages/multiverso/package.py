# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Multiverso(CMakePackage):
    """Multiverso is a parameter server based framework for
    training machine learning models on big data with numbers of machines."""

    homepage = "https://github.com/Microsoft/Multiverso"
    url      = "https://github.com/Microsoft/Multiverso/archive/v0.2.tar.gz"
    git      = "https://github.com/Microsoft/Multiverso.git"

    version('master', branch='master')
    version('143187', commit='143187575d1cfa410100037b8aea2e767e0af637')
    version('0.2', '483ca7524fea14a311389e421f2bc098')

    depends_on('mpi')
    depends_on('boost')

    patch('cmake-143187.patch', when='@143187')

    def cmake_args(self):
        spec = self.spec
        return ['-DBOOST_ROOT:PATH=%s' % spec['boost'].prefix]
