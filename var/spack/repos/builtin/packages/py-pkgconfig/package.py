# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPkgconfig(PythonPackage):
    """Interface Python with pkg-config."""

    homepage = "http://github.com/matze/pkgconfig"
    url      = "https://pypi.io/packages/source/p/pkgconfig/pkgconfig-1.2.2.tar.gz"

    version('1.4.0',  sha256='048c3b457da7b6f686b647ab10bf09e2250e4c50acfe6f215398a8b5e6fcdb52')
    version('1.2.2', sha256='3685ba02a9b72654a764b728b559f327e1dbd7dc6ebc310a1bd429666ee202aa')

    depends_on('python@2.6:')
    depends_on('py-setuptools', type='build')

    depends_on('pkgconfig', type=('build', 'run'))

    depends_on('py-nose@1.0:', type=('build', 'test'))
