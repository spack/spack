# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorchvision(PythonPackage):
    """The torchvision package consists of popular datasets, model
    architectures, and common image transformations for computer vision."""

    homepage = "https://github.com/pytorch/vision"
    url      = "https://github.com/pytorch/vision/archive/v0.3.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'torchvision', 'torchvision.datasets', 'torchvision.models',
        'torchvision.transforms', 'torchvision.ops',
        'torchvision.models.segmentation',
        'torchvision.models.detection'
    ]

    version('0.3.0', sha256='c205f0618c268c6ed2f8abb869ef6eb83e5339c1336c243ad321a2f2a85195f0')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-torch@1.1.0:', type=('build', 'run'))
    depends_on('py-pillow@4.1.1:', type=('build', 'run'))  # or py-pillow-simd

    # Many of the datasets require additional dependencies to use.
    # These can be installed after the fact.
