# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBlosc(PythonPackage):
    """A Python wrapper for the extremely fast Blosc compression library"""

    homepage = "http://python-blosc.blosc.org"
    url      = "https://github.com/Blosc/python-blosc/archive/v1.9.1.tar.gz"
    git      = "https://github.com/Blosc/python-blosc.git"

    version('1.10.2', sha256='fee57fbef7091cc1a0f325e50ce30b7f463bd036ea7bac748315c5449b2e2b24')
    version('1.10.1', sha256='d3238d8ffc13be9848a9a85c80de6f3bfa74bb2000d5614abb5146b25552cca7')
    version('1.10.0', sha256='30605a76853a2eb6b16afbfe63ad1a026562cda4af129128f4ab04a52bac9337')
    version('1.9.2',  sha256='fd03dc3845b2434a3eab57369042388a8ea99f254b8ea494b4b8b1a0595c8a9a')
    version('1.9.1', sha256='ffc884439a12409aa4e8945e21dc920d6bc21807357c51d24c7f0a27ae4f79b9')

    depends_on('cmake@3.11.0:', type='build')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-scikit-build', type='build')
    # depends_on('c-blosc')  # shipped internally
