# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHist(PythonPackage):
    """Hist classes and utilities"""

    homepage = "https://github.com/scikit-hep/hist"
    pypi     = "hist/hist-2.5.2.tar.gz"

    version('2.5.2', sha256='0bafb8b956cc041f1b26e8f5663fb8d3b8f7673f56336facb84d8cfdc30ae2cf')

    variant('plot', default='False',
            description='Add support for drawing histograms')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools@45:', type='build')
    depends_on('py-setuptools-scm@3.4:+toml', type='build')
    depends_on('py-boost-histogram@1.2.0:1.2', type=('build', 'run'))
    depends_on('py-histoprint@2.2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14.5:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7:', type=('build', 'run'), when='^python@:3.7')

    depends_on('py-matplotlib@3.0:', type=('build', 'run'), when='+plot')
    depends_on('py-scipy@1.4:', type=('build', 'run'), when='+plot')
    depends_on('py-iminuit@2:', type=('build', 'run'), when='+plot')
    depends_on('py-mplhep@0.2.16:', type=('build', 'run'), when='+plot')
