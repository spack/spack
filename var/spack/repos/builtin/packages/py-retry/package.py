# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRetry(PythonPackage):
    """Easy to use retry decorator."""

    homepage = "https://github.com/invl/retry"
    pypi     = "retry/retry-0.9.2.tar.gz"

    version('0.9.2', sha256='f8bfa8b99b69c4506d6f5bd3b0aabf77f98cdb17f3c9fc3f5ca820033336fba4')

    depends_on('py-setuptools',         type='build')
