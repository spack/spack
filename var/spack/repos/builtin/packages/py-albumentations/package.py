# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlbumentations(PythonPackage):
    """albumentations is a fast image augmentation library and easy to use wrapper around other libraries."""

    homepage = "https://github.com/albu/albumentations"
    url      = "https://files.pythonhosted.org/packages/f0/08/bd5961340b5bc4dd3b9ac0d8eba04a0cc80b52598b30f1b6842580db8225/albumentations-0.4.2.tar.gz"

    version('1.1.0', sha256='60b067b3093908bcc52adb2aa5d44f57ebdbb8ab57a47b0b42f3dc1d3b1ce824')
    version('0.4.2', sha256='93baec3ca01a61bc81fa80563cdebf35dbae3f86b573e4cbe5c141c94782737f')


    extends('python')

    depends_on('python')

    depends_on('py-setuptools-scm', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('py-torchvision')
    depends_on('py-pyyaml')
    depends_on('py-numpy')
    depends_on('py-torch')
    depends_on('py-scipy')
    depends_on('py-scikit-image')
    depends_on('py-imgaug')
    depends_on('py-imageio')
    depends_on('py-pytest')
    depends_on('opencv')
