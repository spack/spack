# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScikitImage(PythonPackage):
    """Image processing algorithms for SciPy, including IO, morphology,
    filtering, warping, color manipulation, object detection, etc."""

    homepage = "http://scikit-image.org/"
    url      = "https://pypi.io/packages/source/s/scikit-image/scikit-image-0.17.2.tar.gz"

    version('0.17.2', sha256='bd954c0588f0f7e81d9763dc95e06950e68247d540476e06cb77bcbcd8c2d8b3')
    version('0.14.2', sha256='1afd0b84eefd77afd1071c5c1c402553d67be2d7db8950b32d6f773f25850c1f')
    version('0.12.3', sha256='82da192f0e524701e89c5379c79200bc6dc21373f48bf7778a864c583897d7c7')

    extends('python', ignore=r'bin/.*\.py$')

    depends_on('python@3.6:', when='@0.16.1:')
    depends_on('py-dask', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('pil@4.3.0:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-networkx', type=('build', 'run'))
    depends_on('py-networkx@2.0:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.15.1:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scipy@1.0.1:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'), when='@0.14:')
    depends_on('py-pywavelets@1.1.1:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-cloudpickle', type=('build', 'run'), when='@:0.16.1')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.23.4:', type='build')

    conflicts('pil@7.1.0', when='@0.16.1:')
    conflicts('pil@7.1.1', when='@0.16.1:')
    conflicts('py-matplotlib@3.0.0', when='@0.16.1:')
