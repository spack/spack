# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitImage(PythonPackage):
    """Image processing algorithms for SciPy, including IO, morphology,
    filtering, warping, color manipulation, object detection, etc."""

    homepage = "http://scikit-image.org/"
    url      = "https://pypi.io/packages/source/s/scikit-image/scikit-image-0.12.3.tar.gz"

    version('0.14.2', sha256='1afd0b84eefd77afd1071c5c1c402553d67be2d7db8950b32d6f773f25850c1f')
    version('0.12.3', '04ea833383e0b6ad5f65da21292c25e1')

    extends('python', ignore=r'bin/.*\.py$')

    depends_on('py-dask', type=('build', 'run'))
    depends_on('py-pillow', type=('build', 'run'))
    depends_on('py-networkx', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'), when='@0.14:')
    depends_on('py-cloudpickle', type=('build', 'run'), when='@0.14:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.23.4:', type='build')
