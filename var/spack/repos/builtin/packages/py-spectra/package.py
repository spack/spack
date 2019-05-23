# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySpectra(PythonPackage):
    """Color scales and color conversion made easy for Python."""

    homepage = "https://pypi.python.org/pypi/spectra/0.0.8"
    url      = "https://pypi.io/packages/source/s/spectra/spectra-0.0.8.tar.gz"

    version('0.0.11', sha256='8eb362a5187cb63cee13cd01186799c0c791a3ad3bec57b279132e12521762b8')
    version('0.0.8', '83020b29e584389f24c7720f38f0136c')

    depends_on('py-setuptools', type='build')
    depends_on('py-colormath', type=('build', 'run'))
    depends_on('py-colormath@3.0.0:', type=('build', 'run'), when='@0.0.11:')
