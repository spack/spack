# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyminifier(PythonPackage):
    """Pyminifier is a Python code minifier, obfuscator, and compressor."""

    homepage = "http://liftoff.github.io/pyminifier/"
    url      = "https://pypi.io/packages/source/p/pyminifier/pyminifier-2.1.tar.gz"

    version('2.1', 'c1a6b92e69f664005f7adf188c514de7')

    depends_on('py-setuptools', type='build')
