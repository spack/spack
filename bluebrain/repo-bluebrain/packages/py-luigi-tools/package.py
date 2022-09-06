# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    pypi     = 'luigi-tools/luigi-tools-0.0.19.tar.gz'

    version('0.0.19', sha256='322b02909229798aa900170127df44cd689601c594c790e417b054babd9d2bfb')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
