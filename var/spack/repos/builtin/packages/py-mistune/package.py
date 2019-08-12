# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMistune(PythonPackage):
    """
    Python markdown parser
    """
    homepage = "http://mistune.readthedocs.org/en/latest/"
    url      = "https://github.com/lepture/mistune/archive/v0.7.1.tar.gz"

    version('0.7.1', '0d9c29700c670790c5b2471070d32ec2')
    version('0.7', '77750ae8b8d0d584894224a7e0c0523a')
    version('0.6', 'd4f3d4f28a69e715f82b591d5dacf9a6')
    version('0.5.1', '1c6cfce28a4aa90cf125217cd6c6fe6c')
    version('0.5', '997736554f1f95eea78c66ae339b5722')

    depends_on('py-setuptools', type='build')
