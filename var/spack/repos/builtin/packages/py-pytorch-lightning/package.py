# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytorchLightning(PythonPackage):
    """PyTorch Lightning is the lightweight PyTorch wrapper for ML researchers."""

    homepage = "https://github.com/PyTorchLightning/pytorch-lightning"
    pypi     = "pytorch-lightning/pytorch-lightning-1.2.10.tar.gz"

    maintainers = ['adamjstewart']

    version('1.6.0', sha256='1ab6f15750862cfbac48ad7be420050c8c353a060da7c2575f9e267158a33d42')
    version('1.5.3', sha256='a206169a0c4356366a7edadb5ebd2f38e9a611ff78265ce93b767662682f5620')
    version('1.4.1', sha256='1d1128aeb5d0e523d2204c4d9399d65c4e5f41ff0370e96d694a823af5e8e6f3')
    version('1.4.0', sha256='6529cf064f9dc323c94f3ce84b56ee1a05db1b0ab17db77c4d15aa36e34da81f')
    version('1.3.8', sha256='60b0a3e464d394864dae4c8d251afa7aa453644a19bb7672f5ee400343cdf7b0')
    version('1.2.10', sha256='2d8365e30ded0c20e73ce6e5b6028478ae460b8fd33727df2275666df005a301')

    depends_on('python@3.7:', when='@1.6:', type=('build', 'run'))
    depends_on('python@3.6:', when='@:1.5', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.17.2:', when='@1.3:', type=('build', 'run'))
    depends_on('py-numpy@1.16.6:', when='@:1.2', type=('build', 'run'))
    depends_on('py-torch@1.8:', when='@1.6:', type=('build', 'run'))
    depends_on('py-torch@1.6:', when='@1.4:1.5', type=('build', 'run'))
    depends_on('py-torch@1.4:', when='@:1.3', type=('build', 'run'))
    depends_on('py-tqdm@4.41.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.4:', when='@1.6:', type=('build', 'run'))
    depends_on('py-pyyaml@5.1:', when='@1.4:1.5', type=('build', 'run'))
    depends_on('py-pyyaml@5.1:5.4.1', when='@1.3', type=('build', 'run'))
    depends_on('py-pyyaml@5.1:5.3,5.5:', when='@:1.2', type=('build', 'run'))
    depends_on('py-fsspec@2021.05.0:2021.05,2021.06.1:+http', when='@1.3:', type=('build', 'run'))
    depends_on('py-fsspec@0.8.1:+http', when='@:1.2', type=('build', 'run'))
    depends_on('py-tensorboard@2.2.0:', when='@1.5:', type=('build', 'run'))
    depends_on('py-tensorboard@2.2.0:2.4,2.5.1:', when='@:1.4', type=('build', 'run'))
    depends_on('py-torchmetrics@0.4.1:', when='@1.5:', type=('build', 'run'))
    depends_on('py-torchmetrics@0.4.0:', when='@1.4', type=('build', 'run'))
    depends_on('py-torchmetrics@0.2.0:', when='@1.3', type=('build', 'run'))
    depends_on('py-torchmetrics@0.2.0', when='@:1.2', type=('build', 'run'))
    depends_on('py-pydeprecate@0.3.1:0.3', when='@1.6:', type=('build', 'run'))
    depends_on('py-pydeprecate@0.3.1', when='@1.4:1.5', type=('build', 'run'))
    depends_on('py-pydeprecate@0.3.0', when='@1.3', type=('build', 'run'))
    depends_on('py-packaging@17.0:', when='@1.3:', type=('build', 'run'))
    depends_on('py-packaging', when='@:1.2', type=('build', 'run'))
    depends_on('py-typing-extensions@4:', when='@1.6:', type=('build', 'run'))
    depends_on('py-typing-extensions', when='@1.4:1.5', type=('build', 'run'))
    depends_on('py-future@0.17.1:', when='@:1.5', type=('build', 'run'))
    depends_on('pil@:8.2,8.3.1:', when='@1.3', type=('build', 'run'))
