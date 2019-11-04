# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://www.example.com"
    url      = "https://pypi.io/packages/source/p/pre_commit/pre_commit-1.20.0.tar.gz"

    version('1.20.0', sha256='9f152687127ec90642a2cc3e4d9e1e6240c4eb153615cb02aa1ad41d331cbb6e')

    depends_on('py-setuptools', type='build')
