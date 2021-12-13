# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZipfileDeflate64(PythonPackage):
    """Extract Deflate64 ZIP archives with Python's zipfile API."""

    homepage = "https://github.com/brianhelba/zipfile-deflate64"
    pypi     = "zipfile-deflate64/zipfile-deflate64-0.1.6.tar.gz"

    version('0.1.6', sha256='792c7fc904740be3197b70afdd82a931f8dbec6db38d7b5be74c3ffbbed75a96')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools-scm@3.4:+toml', type='build')
