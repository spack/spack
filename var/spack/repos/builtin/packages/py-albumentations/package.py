# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlbumentations(PythonPackage):
    """albumentations is a fast image augmentation library and easy to use wrapper around other libraries."""

    homepage = "https://github.com/albu/albumentations"
    url      = "https://files.pythonhosted.org/packages/c8/a2/ab0ddadd960b4caf824063783d24174119cbddae409ff99fbe6fd45c63ec/albumentations-1.1.0.tar.gz"

    version('1.1.0', sha256='60b067b3093908bcc52adb2aa5d44f57ebdbb8ab57a47b0b42f3dc1d3b1ce824')
    version('0.4.2', sha256='93baec3ca01a61bc81fa80563cdebf35dbae3f86b573e4cbe5c141c94782737f')


    extends('python')

    depends_on('python')

    depends_on('py-setuptools-scm', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('py-torchvision', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-torch', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-imgaug', type=('build', 'run'))
    depends_on('py-imageio', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('opencv', type=('build', 'run'))
