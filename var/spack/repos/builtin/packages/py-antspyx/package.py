# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAntspyx(PythonPackage):
    """Advanced Normalization Tools in Python."""

    homepage = "https://pypi.org/project/antspyx/"
    url = "https://github.com/ANTsX/ANTsPy/archive/refs/tags/v0.2.7.tar.gz"

    version('0.2.7', sha256='495868dcb975486203cd1ce901c803e4b5d71fad5ad5c2525612de8e030f6a34')
    version('0.2.4', sha256='357d9f93fdac8ca76f660d23f97239a5949284664866f8ba254b912afa953e55')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('cmake', type='build')
    depends_on('itk')

    depends_on('py-pandas', type=('run'))
    depends_on('py-numpy', type=('run'))
    depends_on('py-scipy', type=('run'))
    depends_on('py-scikit-image', type=('run'))
    depends_on('py-scikit-learn', type=('run'))
    depends_on('py-statsmodels', type=('run'))
    depends_on('py-webcolors', type=('run'))
    depends_on('py-matplotlib', type=('run'))
    depends_on('py-pyyaml', type=('run'))
    depends_on('py-chart-studio', type=('run'))
    depends_on('py-pillow', type=('run'))
    depends_on('py-nibabel', type=('run'))

    patch('setup-purge-sklearn.diff', when='@0.2.7')
