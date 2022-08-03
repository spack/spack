# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigspace(PythonPackage):
    """Creation and manipulation of parameter configuration spaces for
       automated algorithm configuration and hyperparameter tuning."""

    maintainers = ['Kerilk']

    homepage = "https://automl.github.io/ConfigSpace/master/"
    pypi     = "ConfigSpace/ConfigSpace-0.4.20.tar.gz"

    version('0.4.20', sha256='2e4ca06f5a6a61e5322a73dd7545468c79f2a3e8385cab92fdada317af41d9e9')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('py-pyparsing', type=('build', 'run'))
