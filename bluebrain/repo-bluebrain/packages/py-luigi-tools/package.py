# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    url      = 'https://pypi.io/packages/source/l/luigi-tools/luigi-tools-0.0.15.tar.gz'

    version('0.0.15', sha256='4ba9b2877fed76bfb70d5b203cd47c5d805e5dbeb7760a1c0771d892e8567fcf')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
