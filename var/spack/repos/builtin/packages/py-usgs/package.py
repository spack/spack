# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUsgs(PythonPackage):
    """Client library for interfacing with USGS datasets"""

    homepage = "https://github.com/kapadia/usgs"
    url      = "https://pypi.org/packages/source/u/usgs/usgs-0.2.7.tar.gz"

    version('0.2.7', sha256='484e569ea1baf9574e11ccf15219957364690dcf06ee3d09afef030df944e79b')

    depends_on('py-setuptools', type='build')
    depends_on('py-mock', type='test')
    depends_on('py-pytest@2.8.7', type='test')
    depends_on('py-click@4.0:', type=('build', 'run'))
    depends_on('py-requests@2.7.0:', type=('build', 'run'))
    depends_on('py-requests-futures@0.9.5:', type=('build', 'run'))
