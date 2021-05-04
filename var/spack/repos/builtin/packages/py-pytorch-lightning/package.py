# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytorchLightning(PythonPackage):
    """PyTorch Lightning is the lightweight PyTorch wrapper for ML researchers."""

    homepage = "https://github.com/PyTorchLightning/pytorch-lightning"
    pypi     = "pytorch-lightning/pytorch-lightning-1.2.10.tar.gz"

    version('1.2.10', sha256='2d8365e30ded0c20e73ce6e5b6028478ae460b8fd33727df2275666df005a301')

    conflicts('py-pyyaml@5.4')          # OmegaConf requirement >=5.1
    conflicts('py-tensorboard@2.5.0')   # 2.5.0 GPU CI error: Couldn't build proto file into descriptor pool!

    # requirements from setup.py
    depends_on('py-setuptools',             type='build')
    depends_on('python@3.6:',               type=('build', 'run'))
    depends_on('py-torch@1.4:',             type=('build', 'run'))
    depends_on('py-numpy@1.16.6:',          type=('build', 'run'))
    depends_on('py-future@0.17.1:',         type=('build', 'run'))
    depends_on('py-pyyaml@5.1:',            type=('build', 'run'))
    depends_on('py-tqdm@4.41.0:',           type=('build', 'run'))
    depends_on('py-fsspec@0.8.1:+http',     type=('build', 'run'))
    depends_on('py-tensorboard@2.2.0:',     type=('build', 'run'))
    depends_on('py-torchmetrics@0.2.0',     type=('build', 'run'))
    depends_on('py-packaging',              type=('build', 'run'))
