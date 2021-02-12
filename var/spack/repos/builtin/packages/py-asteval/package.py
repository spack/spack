# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAsteval(PythonPackage):
    """Safe, minimalistic evaluator of python expression using ast module"""

    homepage = "http://github.com/newville/asteval"
    pypi = "asteval/asteval-0.9.18.tar.gz"

    version('0.9.22', sha256='74a0939765fc6b1421e6672ccf74c52edc3c7af7d6a8298b057b0d50ac51aea8')
    version('0.9.21', sha256='ee14ba2211cda1c76114e3e7b552cdd57e940309203d5f4106e6d6f2c2346a2e')
    version('0.9.20', sha256='6b8a389e5215e257bcdc7bef9526558775f6e276cb2d7473fe53c6d8227a2528')
    version('0.9.19', sha256='445f3a59df692c0c0ff2868c0bbf9b293884db4a9f9a13c73555485ba75ed08b')
    version('0.9.18', sha256='5d64e18b8a72c2c7ae8f9b70d1f80b68bbcaa98c1c0d7047c35489d03209bc86')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
