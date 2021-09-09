# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImgaug(PythonPackage):
    """A library for image augmentation in machine learning experiments,
    particularly convolutional neural networks. Supports the augmentation of
    images, keypoints/landmarks, bounding boxes, heatmaps and segmentation maps
    in a variety of different ways."""

    homepage = "https://github.com/aleju/imgaug"
    pypi     = "imgaug/imgaug-0.3.0.tar.gz"

    version('0.3.0', sha256='e1354d41921f1b306b50c5141b4870f17e81b531cae2f5c3093da9dc4dcb3cf4')

    extends('python')

    depends_on('py-setuptools', type='build')
    depends_on('py-gmpy2', type=('build', 'run'))
    depends_on('py-imageio', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-mock', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-shapely', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
