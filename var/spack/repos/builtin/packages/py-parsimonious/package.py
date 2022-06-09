# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParsimonious(PythonPackage):
    """(Soon to be) the fastest pure-Python PEG parser"""

    homepage = "https://github.com/erikrose/parsimonious"
    pypi     = "parsimonious/parsimonious-0.8.1.tar.gz"

    version('0.8.1', sha256='3add338892d580e0cb3b1a39e4a1b427ff9f687858fdd61097053742391a9f6b')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:',        type=('build', 'run'))
