# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPkgconfig(PythonPackage):
    """Interface Python with pkg-config."""

    homepage = "http://github.com/matze/pkgconfig"
    url      = "https://pypi.io/packages/source/p/pkgconfig/pkgconfig-1.2.2.tar.gz"

    version('1.2.2', '81a8f6ef3371831d081e03db39e09683')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')

    depends_on('pkgconfig', type=('build', 'run'))

    depends_on('py-nose@1.0:', type=('build', 'test'))
