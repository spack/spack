# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMachotools(PythonPackage):
    """Python package for editing Mach-O headers using macholib"""

    homepage = "https://pypi.python.org/pypi/machotools"
    url = "https://pypi.io/packages/source/m/machotools/machotools-0.2.0.tar.gz"

    version('0.2.0', 'bcc68332c4a80b4f84ec9c8083465416')

    depends_on('py-setuptools', type='build')
    depends_on('py-macholib', type=('build', 'run'))
