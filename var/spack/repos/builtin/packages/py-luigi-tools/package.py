# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLuigiTools(PythonPackage):
    '''Tools to work with luigi.'''

    homepage = 'https://github.com/BlueBrain/luigi-tools'
    url      = 'https://pypi.io/packages/source/l/luigi-tools/luigi-tools-0.0.12.tar.gz'

    version('0.0.12', sha256='761c8b7cbee56d3a6e133f769f064f8b700cd08da829c313f9bea5046b1dcdc3')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-luigi', type='run')
