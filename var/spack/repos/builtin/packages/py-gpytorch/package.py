# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGpytorch(PythonPackage):
    """GPyTorch is a Gaussian process library implemented using PyTorch.
    GPyTorch is designed for creating scalable, flexible, and modular Gaussian
    process models with ease."""

    homepage = "https://gpytorch.ai/"
    url      = "https://pypi.io/packages/source/g/gpytorch/gpytorch-1.1.1.tar.gz"

    maintainers = ['adamjstewart']

    version('1.1.1', sha256='76bd455db2f17af5425f73acfaa6d61b8adb1f07ad4881c0fa22673f84fb571a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-torch@1.5:', type=('build', 'run'))
