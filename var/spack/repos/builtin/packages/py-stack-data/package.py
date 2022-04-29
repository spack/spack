# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyStackData(PythonPackage):
    """Extract data from python stack frames and tracebacks for informative
    displays."""

    homepage = "http://github.com/alexmojaki/stack_data"
    pypi     = "stack_data/stack_data-0.2.0.tar.gz"

    version('0.2.0', sha256='45692d41bd633a9503a5195552df22b583caf16f0b27c4e58c98d88c8b648e12')

    depends_on('py-setuptools@44:', type='build')
    depends_on('py-setuptools-scm+toml@3.4.3:', type='build')
    depends_on('py-executing', type=('build', 'run'))
    depends_on('py-asttokens', type=('build', 'run'))
    depends_on('py-pure-eval', type=('build', 'run'))
