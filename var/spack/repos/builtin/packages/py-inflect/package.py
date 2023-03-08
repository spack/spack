# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInflect(PythonPackage):
    """inflect.py - Correctly generate plurals, singular nouns, ordinals,
    indefinite articles; convert numbers to words."""

    homepage = "https://github.com/jaraco/inflect"
    pypi = "inflect/inflect-5.0.2.tar.gz"

    version('5.0.2', sha256='d284c905414fe37c050734c8600fe170adfb98ba40f72fc66fed393f5b8d5ea0')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on("py-setuptools-scm+toml@3.4.1:", type="build")
