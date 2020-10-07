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
    depends_on('py-dask', type=('run'), when='@:0.14.2')
    depends_on('pil', type=('run'))
    depends_on('pil@4.3:7.0,7.1.2:', type=('build', 'run'), when='@0.16:')
    depends_on('py-networkx', type=('run'))
    depends_on('py-networkx@2.0:', type=('run'), when='@0.16.1:')
    depends_on('py-six', type=('build', 'run'), when='@:0.15.1')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numpy@1.14.1:', type=('build', 'run'), when='@0.16.1:')
    depends_on('py-numpy@1.15.1:', type=('build', 'run'), when='@0.17.1:')
    depends_on('py-scipy', type=('run'))
    depends_on('py-scipy@0.19.0:', type=('run'), when='@0.16.1:')
    depends_on('py-scipy@1.0.1:', type=('run'), when='@0.17.1:')
    depends_on('py-cython@0.23.4:', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-matplotlib@2.0.0:2.9.999,3.0.1:', type=('run'), when='@0.16.1:')
    depends_on('py-imageio@2.0.1:', type=('run'), when='@0.15.1:')
    depends_on('py-imageio@2.3.0:', type=('run'), when='@0.16.1:')
    depends_on('py-tifffile@2019.7.26:', type=('run'), when='@0.17.1:')
    depends_on('py-pywavelets', type=('run'), when='@0.14:')
    depends_on('py-pywavelets@1.1.1:', type=('run'), when='@0.16.1:')
