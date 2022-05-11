# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVector(PythonPackage):
    """Vector classes and utilities"""

    homepage = "https://github.com/scikit-hep/vector"
    pypi     = "vector/vector-0.8.4.tar.gz"

    version('0.8.4', sha256='ef97bfec0263766edbb74c290401f89921f8d11ae9e4a0ffd904ae40674f1239')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:',            type='build')
    depends_on('py-setuptools-scm@3.4: +toml', type='build')
    depends_on('py-wheel',                     type='build')
    depends_on('py-numpy@1.13.3:',             type=('build', 'run'))
    depends_on('py-packaging@19.0:',           type=('build', 'run'))
    depends_on('py-importlib-metadata@0.22:',  type=('build', 'run'), when='^python@:3.7')
    depends_on('py-typing-extensions',         type=('build', 'run'), when='^python@:3.7')
