# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTorchvision(PythonPackage):
    """The torchvision package consists of popular datasets, model
    architectures, and common image transformations for computer vision."""

    homepage = "https://github.com/pytorch/vision"
    url      = "https://github.com/pytorch/vision/archive/v0.6.0.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'torchvision', 'torchvision.datasets', 'torchvision.models',
        'torchvision.transforms', 'torchvision.ops',
        'torchvision.models.segmentation',
        'torchvision.models.detection'
    ]

    version('0.6.0', sha256='02de11b3abe6882de4032ce86dab9c7794cbc84369b44d04e667486580f0f1f7')
    version('0.5.0', sha256='eb9afc93df3d174d975ee0914057a9522f5272310b4d56c150b955c287a4d74d')
    version('0.4.2', sha256='1184a27eab85c9e784bacc6f9d6fec99e168ab4eda6047ef9f709e7fdb22d8f9')
    version('0.4.1', sha256='053689351272b3bd2ac3e6ba51efd284de0e4ca4a301f54674b949f1e62b7176')
    version('0.4.0', sha256='c270d74e568bad4559fed4544f6dd1e22e2eb1c60b088e04a5bd5787c4150589')
    version('0.3.0', sha256='c205f0618c268c6ed2f8abb869ef6eb83e5339c1336c243ad321a2f2a85195f0')

    depends_on('python@3:', when='@0.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', when='@:0.5', type=('build', 'run'))
    depends_on('py-torch@1.4:', when='@0.6:', type=('build', 'link', 'run'))
    depends_on('py-torch@1.2:', when='@0.4:', type=('build', 'link', 'run'))
    depends_on('py-torch@1.1:', type=('build', 'link', 'run'))
    # https://github.com/pytorch/vision/issues/1712
    depends_on('py-pillow@4.1.1:6', when='@:0.4', type=('build', 'run'))  # or py-pillow-simd
    depends_on('py-pillow@4.1.1:',  when='@0.5:', type=('build', 'run'))  # or py-pillow-simd

    # Many of the datasets require additional dependencies to use.
    # These can be installed after the fact.
    depends_on('py-scipy', type='test')
