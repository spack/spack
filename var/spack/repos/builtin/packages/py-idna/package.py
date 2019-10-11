# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46) """

    homepage = "https://github.com/kjd/idna"
    url      = "https://pypi.io/packages/source/i/idna/idna-2.5.tar.gz"

    version('2.5', sha256='3cb5ce08046c4e3a560fc02f138d0ac63e00f8ce5901a56b32ec8b7994082aab')

    depends_on('py-setuptools', type=('build', 'link'))
    depends_on('python@2.6:',   type=('build', 'run'))
