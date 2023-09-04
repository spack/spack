# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PytorchRandaugment(PythonPackage):
    """Unofficial PyTorch Reimplementation of AutoAugment and RandAugment."""

    homepage = "https://github.com/jizongFox/pytorch-randaugment"
    url = "https://files.pythonhosted.org/packages/ac/a3/0d76507a2048b38fe9cc77f85b8ac008543b0c2c237feb5a1a1a882d46aa/randaugment-1.0.2.tar.gz"

    maintainers("sthalles")

    version("1.0.2", md5="dd7106ba907eb0ad2b239e240d4e97c9")

    depends_on("py-pip", type='build')
    depends_on("py-setuptools", type='build')
    depends_on("py-wheel", type='build')
    depends_on("python", type=('build', 'run'))
    depends_on("py-torch", type=('build', 'run'))
    depends_on("py-torchvision", type=('build','run'))
