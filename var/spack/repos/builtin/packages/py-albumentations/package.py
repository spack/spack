# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlbumentations(PythonPackage):
    """albumentations is a fast image augmentation library and
    easy to use wrapper around other libraries."""

    homepage = "https://github.com/albu/albumentations"
    url      = "https://files.pythonhosted.org/packages/c8/a2/ab0ddadd960b4caf824063783d24174119cbddae409ff99fbe6fd45c63ec/albumentations-1.1.0.tar.gz"

    version('1.1.0', sha256='60b067b3093908bcc52adb2aa5d44f57ebdbb8ab57a47b0b42f3dc1d3b1ce824')
    version('0.4.2', sha256='93baec3ca01a61bc81fa80563cdebf35dbae3f86b573e4cbe5c141c94782737f')

    depends_on('python@3.6:',                 type=('build', 'run'), when='@1.1.0:')
    depends_on('py-setuptools',               type='build')
    depends_on('py-numpy@1.11.1:',            type=('build', 'run'))
    depends_on('py-scipy',                    type=('build', 'run'))
    depends_on('py-imgaug@0.2.5:0.2.6',       type=('build', 'run'), when='@0.4.2')
    depends_on('py-scikit-image@0.16.1:1.18', type=('build', 'run'), when='@1.1.0:')
    depends_on('py-pyyaml',                   type=('build', 'run'))
    depends_on('py-qudida@0.0.4:',            type=('build', 'run'), when='@1.1.0:')
    depends_on('opencv@4.1.1:+python2',       type=('build', 'run'), when='^python@2.0:2')
    depends_on('opencv@4.1.1:+python3',       type=('build', 'run'), when='^python@3.0:3')
