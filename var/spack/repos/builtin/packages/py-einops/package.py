# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEinops(PythonPackage):
    """Flexible and powerful tensor operations for readable and reliable code.

    Supports numpy, pytorch, tensorflow, and others."""

    homepage = "https://github.com/arogozhnikov/einops"
    pypi     = "einops/einops-0.3.2.tar.gz"

    version('0.3.2', sha256='5200e413539f0377f4177ef00dc019968f4177c49b1db3e836c7883df2a5fe2e')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
