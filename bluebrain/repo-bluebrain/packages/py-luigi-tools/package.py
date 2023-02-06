# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    pypi = 'luigi-tools/luigi-tools-0.2.1.tar.gz'

    version('0.2.1', sha256='901fa0ee119b52f4b78cf54dc72c07e93288237b86f14fd473f8dfe2fd28ffa4')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
    depends_on('py-jsonschema', type='run')
    depends_on('py-typing-extensions', type='run')
