# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    pypi     = 'luigi-tools/luigi-tools-0.0.17.tar.gz'

    version('0.0.17', sha256='f234b2fd493a966ab5ae8441ce26c910a35339badd2b4493f4b1fa54abc1bef0')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
