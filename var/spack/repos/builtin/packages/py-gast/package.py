# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGast(PythonPackage):
    """Python AST that abstracts the underlying Python version"""

    homepage = "https://github.com/serge-sans-paille/gast"
    url      = "https://pypi.io/packages/source/g/gast/gast-0.3.2.tar.gz"

    version('0.3.2', sha256='5c7617f1f6c8b8b426819642b16b9016727ddaecd16af9a07753e537eba8a3a5')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
