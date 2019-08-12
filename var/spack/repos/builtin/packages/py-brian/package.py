# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBrian(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "http://www.briansimulator.org"
    url      = "https://pypi.io/packages/source/b/brian/brian-1.4.3.tar.gz"

    version('1.4.3', '0570099bcce4d7afde73ff4126e6c30f')

    depends_on('py-matplotlib@0.90.1:', type=('build', 'run'))
    depends_on('py-numpy@1.4.1:',       type=('build', 'run'))
    depends_on('py-scipy@0.7.0:',       type=('build', 'run'))
