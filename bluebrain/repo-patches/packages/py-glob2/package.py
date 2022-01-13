# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyGlob2(PythonPackage):
    """This is an extended version of Python's builtin glob module.
    """

    homepage = "https://github.com/miracle2k/python-glob2"
    url = "https://pypi.io/packages/source/g/glob2/glob2-0.7.tar.gz"

    version('0.7', sha256='85c3dbd07c8aa26d63d7aacee34fa86e9a91a3873bc30bf62ec46e531f92ab8c')

    depends_on('py-setuptools', type='build')
