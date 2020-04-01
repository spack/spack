# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyInvoke(PythonPackage):
    """Pythonic task execution"""

    homepage = "http://www.pyinvoke.org/"
    url      = "https://pypi.io/packages/source/i/invoke/invoke-1.2.0.tar.gz"

    version('1.2.0', sha256='dc492f8f17a0746e92081aec3f86ae0b4750bf41607ea2ad87e5a7b5705121b7')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
