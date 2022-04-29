# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *

# Package automatically generated using 'pip2spack' converter


class PySelectors34(PythonPackage):
    """
    Backport of the selectors module from Python 3.4.
    """

    homepage = "https://github.com/berkerpeksag/selectors34"
    pypi = 'selectors34/selectors34-1.2.tar.gz'
    maintainers = ['liuyangzhuan']

    version('1.2', sha256='09f5066337f8a76fb5233f267873f89a27a17c10bf79575954894bb71686451c')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
