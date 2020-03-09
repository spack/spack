# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCloudpickle(PythonPackage):
    """Extended pickling support for Python objects."""

    homepage = "https://github.com/cloudpipe/cloudpickle"
    url      = "https://pypi.io/packages/source/c/cloudpickle/cloudpickle-0.5.2.tar.gz"

    import_modules = ['cloudpickle']

    version('1.2.1', sha256='603244e0f552b72a267d47a7d9b347b27a3430f58a0536037a290e7e0e212ecf')
    version('0.5.2', sha256='b0e63dd89ed5285171a570186751bc9b84493675e99e12789e9a5dc5490ef554')

    depends_on('py-setuptools', type='build')

    def test(self):
        # PyPI tarball does not come with unit tests
        pass
