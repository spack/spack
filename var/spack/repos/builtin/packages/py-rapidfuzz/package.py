# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRapidfuzz(PythonPackage):
    """Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance."""

    homepage = "https://github.com/maxbachmann/rapidfuzz"
    pypi     = "rapidfuzz/rapidfuzz-1.8.2.tar.gz"

    version('1.8.2', sha256='d6efbb2b6b18b3a67d7bdfbcd9bb72732f55736852bbef823bdf210f9e0c6c90')

    depends_on('python@2.7:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
