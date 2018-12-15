# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46) """

    homepage = "https://github.com/kjd/idna"
    url      = "https://pypi.io/packages/source/i/idna/idna-2.5.tar.gz"

    version('2.5', 'fc1d992bef73e8824db411bb5d21f012')

    depends_on('py-setuptools', type=('build', 'link'))
    depends_on('python@2.6:',   type=('build', 'run'))
