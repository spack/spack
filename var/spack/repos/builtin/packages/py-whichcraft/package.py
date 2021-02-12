# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWhichcraft(PythonPackage):
    """Cross-platform cross-python shutil.which functionality."""

    homepage = "https://github.com/pydanny/whichcraft"
    url      = "https://github.com/pydanny/whichcraft/archive/0.4.1.tar.gz"

    version('0.6.1', sha256='bfa077578261e8bce72ebd44025a2ac196f943123e551589bd5f1c25af9f0085')
    version('0.6.0', sha256='9fa0f8ff6c9d86eacb25897ec307ad154e3e03231cb5be36a192c135004e289f')
    version('0.5.2', sha256='1c694bf3a2cfb1a61e3b3f3ebe33bedb96fbb034a37cc62b180248ccbd852b6f')
    version('0.5.1', sha256='e4b9cf6596ae9ac7eee67f8345f139e493a2d78e4093d6c03ad4f468f0a8bce8')
    version('0.5.0', sha256='5e1c553cf968025335fd549468f772ce3bae1375866b466e3c04c59a28cf3ad3')
    version('0.4.1', sha256='66875022b3b9da8ddf7ab236c15670a782094550d07daeb51ceba4bc61b6b4aa')

    depends_on('py-setuptools', type='build')
