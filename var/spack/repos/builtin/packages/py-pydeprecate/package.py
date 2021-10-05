# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydeprecate(PythonPackage):
    """Simple tooling for marking deprecated functions or classes and re-routing
    to the new successors' instance."""

    homepage = "https://borda.github.io/pyDeprecate/"
    pypi     = "pyDeprecate/pyDeprecate-0.3.0.tar.gz"

    version('0.3.0', sha256='335742ec53b9d22a0a9ff4f3470300c94935f6e169c74b08aee14d871ca40e00')

    depends_on('python@3.6:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
