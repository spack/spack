# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    pypi     = 'luigi-tools/luigi-tools-0.0.16.tar.gz'

    version('0.0.16', sha256='c0cc4c220dd6604671234614378082596825416da630735763f7fc6f6ef853bb')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
