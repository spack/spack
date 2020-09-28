# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCrcmod(PythonPackage):
    """Python module for generating objects that
       compute the Cyclic Redundancy Check (CRC)"""

    homepage = "https://github.com/gsutil-mirrors/crcmod"
    url      = "https://files.pythonhosted.org/packages/c1/35/f63f75068e1e9c4b54522c3fefb7134b5d91917fdc33f17e2889e0f4590c/crcmod-1.6.tar.gz"

    version('1.6', sha256='56d27d035ea029c6ed96779ca042c0136d39d106e3c30baa6422738c7d86aaa5')

    depends_on('python@2.4:2.7,3.1:', type=('build', 'run'))
    depends_on('py-setuptools@40.0.0', type='build')

    def install(self, spec, prefix):
        # Override install to avoid
        #   error: option --single-version-externally-managed not recognized
        setup_py('install', '--root=/', '--prefix={0}'.format(prefix))
