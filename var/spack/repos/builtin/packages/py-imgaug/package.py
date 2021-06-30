# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImgaug(PythonPackage):
    """Image augmentation library for deep neural networks."""

    homepage = "https://pypi.org/project/imgaug/"
    url = "https://files.pythonhosted.org/packages/4f/96/c55f2985b464ea377238e61026dfb1da54d8edc1534c649e70077e94c642/imgaug-0.2.9.tar.gz"

    version('0.2.9', sha256='42b0c4c8cbe197d4f5dbd33960a1140f8a0d9c22c0a8851306ecbbc032092de8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-six', type=('run'))
    depends_on('py-numpy@1.15:', type=('run'))
    depends_on('py-scipy', type=('run'))
    depends_on('py-pillow', type=('run'))
    depends_on('py-matplotlib', type=('run'))
    depends_on('py-scikit-image@0.14.2:', type=('run'))
    depends_on('opencv +python', type=('run'))
    depends_on('py-imageio', type=('run'))
    depends_on('py-shapely', type=('run'))
