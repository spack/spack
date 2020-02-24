# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetuptoolsScm(PythonPackage):
    """The blessed package to manage your versions by scm tags."""

    homepage = "https://github.com/pypa/setuptools_scm"
    url      = "https://pypi.io/packages/source/s/setuptools_scm/setuptools_scm-3.3.3.tar.gz"

    import_modules = ['setuptools_scm']

    version('3.3.3',  sha256='bd25e1fb5e4d603dcf490f1fde40fb4c595b357795674c3e5cb7f6217ab39ea5')
    version('3.1.0',  sha256='1191f2a136b5e86f7ca8ab00a97ef7aef997131f1f6d4971be69a1ef387d8b40')
    version('1.15.6', sha256='49ab4685589986a42da85706b3311a2f74f1af567d39fee6cb1e088d7a75fb5f')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
