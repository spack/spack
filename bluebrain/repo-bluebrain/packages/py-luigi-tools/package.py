# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    pypi     = 'luigi-tools/luigi-tools-0.0.18.tar.gz'

    version('0.0.18', sha256='14a0f493ad2069e71cff2a0f776c1b5535cc7c942124d0adb9d15d63907c930d')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
