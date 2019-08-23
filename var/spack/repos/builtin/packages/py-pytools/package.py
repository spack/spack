# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytools(PythonPackage):
    """A collection of tools for Python"""

    homepage = "https://pypi.org/project/pytools/"
    url      = "https://pypi.io/packages/source/p/pytools/pytools-2019.1.1.tar.gz"

    version('2019.1.1', sha256='ce2d702ae4ef10a70197b00b93141461140d00578f2a862fa946ca1446a300db')

    depends_on('py-setuptools', type='build')
    depends_on('py-decorator@3.2.0:', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:', type=('build', 'run'))
    depends_on('py-six@1.8.0:', type=('build', 'run'))
    depends_on('py-numpy@1.6.0:', type=('build', 'run'))
