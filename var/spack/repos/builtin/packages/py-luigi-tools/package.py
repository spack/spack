# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://bbpcode.epfl.ch/code/#/admin/projects/common/luigi-tools'
    git      = 'ssh://bbpcode.epfl.ch/common/luigi-tools'

    version('0.0.7', tag='luigi-tools-v0.0.7')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
