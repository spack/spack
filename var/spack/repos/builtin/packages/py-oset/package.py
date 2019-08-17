# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOset(PythonPackage):
    """Set that remembers original insertion order."""

    homepage = "https://pypi.python.org/pypi/oset"
    url      = "https://pypi.io/packages/source/o/oset/oset-0.1.3.tar.gz"

    import_modules = ['oset']

    version('0.1.3', 'f23e5a545d2c77df3916398d2d39a3ab')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.5:', type=('build', 'run'))
