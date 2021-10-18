# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBigdft(PythonPackage):
    """BigDFT: electronic structure calculation based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url      = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.1/bigdft-suite-1.9.1.tar.gz"
    git      = "https://gitlab.com/l_sim/bigdft-suite.git"

    version('develop', branch='develop')
    version('1.9.1',   sha256='3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41')
    version('1.9.0',   sha256='4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8')

    depends_on('python@3.7:')
    depends_on('py-setuptools')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        python = which('python')

        with working_dir('PyBigDFT'):
            python('setup.py', 'build')

    def install(self, spec, prefix):
        python = which('python')

        with working_dir('PyBigDFT'):
            python('setup.py', 'install', '--prefix=%s' % prefix)