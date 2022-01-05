# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDateutil(PythonPackage):
    """Extensions to the standard Python datetime module."""
    homepage = "https://pypi.org/project/python-dateutil"
    url      = "https://pypi.io/packages/source/p/python-dateutil/python-dateutil-2.4.0.tar.gz"

    version('2.2', sha256='eec865307ebe7f329a6a9945c15453265a449cdaaf3710340828a1934d53e468')
    version('2.4.0', sha256='439df33ce47ef1478a4f4765f3390eab0ed3ec4ae10be32f2930000c8d19f417')
    version('2.4.2', sha256='3e95445c1db500a344079a47b171c45ef18f57d188dffdb0e4165c71bea8eb3d')
    version('2.5.2', sha256='063907ef47f6e187b8fe0728952e4effb587a34f2dc356888646f9b71fbb2e4b')
    version('2.8.0', sha256='c89805f6f4d64db21ed966fda138f8a5ed7a4fdbc1a8ee329ce1b74e3c74da9e')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-six', type=('build', 'run'))
