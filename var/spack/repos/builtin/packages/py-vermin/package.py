# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVermin(PythonPackage):
    """Concurrently detect the minimum Python versions needed to run code."""

    homepage = "https://github.com/netromdk/vermin"
    url      = "https://github.com/netromdk/vermin/archive/v0.10.0.tar.gz"

    import_modules = ['vermin']

    version('0.10.0', sha256='3458a4d084bba5c95fd7208888aaf0e324a07ee092786ee4e5529f539ab4951f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    def test(self):
        make('test')
