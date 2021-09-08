# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    url      = "https://pypi.io/packages/source/f/fasteners/fasteners-0.16.3.tar.gz"

    version('0.16.3', sha256='b1ab4e5adfbc28681ce44b3024421c4f567e705cc3963c732bf1cba3348307de')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.6:',   type=('build', 'run'))
