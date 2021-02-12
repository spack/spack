# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColorama(PythonPackage):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    pypi = "colorama/colorama-0.3.7.tar.gz"

    version('0.4.4', sha256='5941b2b48a20143d2267e95b1c2a7603ce057ee39fd88e7329b0c292aa16869b')
    version('0.4.3', sha256='e96da0d330793e2cb9485e9ddfd918d456036c7149416295932478192f4436a1')
    version('0.4.2', sha256='3e0d36a97e86c019317b4896075b38a72438df68abdde0518a6ca12c88448a4b')
    version('0.4.1', sha256='05eed71e2e327246ad6b38c540c4a3117230b19679b875190486ddd2d721422d')
    version('0.3.7', sha256='e043c8d32527607223652021ff648fbb394d5e19cba9f1a698670b338c9d782b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
