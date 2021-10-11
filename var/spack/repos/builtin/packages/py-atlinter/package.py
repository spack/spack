# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, variant, version


class PyAtlinter(PythonPackage):
    """Interpolation of section images."""

    homepage = 'https://bbpgitlab.epfl.ch/project/proj101/atlas_interpolation'
    git = 'git@bbpgitlab.epfl.ch:project/proj101/atlas_interpolation.git'

    maintainers = ['EmilieDel', 'Stannislav']

    version('0.1.0', commit='4339279b40d04716d3385e1c5dbd666359ec3fa1')

    variant('cuda', default=False, description='Enable CUDA support')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-atldld@0.2.2', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-pillow', type='run')
    depends_on('py-pytorch-fid', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-torch+cuda', when='+cuda', type='run')
    depends_on('py-torch~cuda~cudnn~nccl', when='~cuda', type='run')
    depends_on('py-torchvision', type='run')
