# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySegmentationModelsPytorch(PythonPackage):
    """Python library with Neural Networks for Image Segmentation based on PyTorch."""

    homepage = "https://github.com/qubvel/segmentation_models.pytorch"
    pypi     = "segmentation_models_pytorch/segmentation_models_pytorch-0.2.0.tar.gz"

    version('0.2.0', sha256='247266722c23feeef16b0862456c5ce815e5f0a77f95c2cd624a71bf00d955df')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-torchvision@0.5.0:', type=('build', 'run'))
    depends_on('py-pretrainedmodels@0.7.4', type=('build', 'run'))
    depends_on('py-efficientnet-pytorch@0.6.3', type=('build', 'run'))
    depends_on('py-timm@0.4.12', type=('build', 'run'))
