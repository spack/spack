# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKornia(PythonPackage):
    """Open Source Differentiable Computer Vision Library for PyTorch."""

    homepage = "https://www.kornia.org/"
    pypi     = "kornia/kornia-0.5.10.tar.gz"

    version('0.5.10', sha256='428b4b934a2ba7360cc6cba051ed8fd96c2d0f66611fdca0834e82845f14f65d')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-torch@1.6.0:', type=('build', 'run'))
