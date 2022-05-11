# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyCookies(PythonPackage):
    """Friendlier RFC 6265-compliant cookie parser/renderer"""

    homepage = "https://github.com/sashahart/cookies"
    pypi     = "cookies/cookies-2.2.1.tar.gz"

    maintainers = ['dorton21']

    version('2.2.1', sha256='d6b698788cae4cfa4e62ef8643a9ca332b79bd96cb314294b864ae8d7eb3ee8e')

    depends_on('py-setuptools', type='build')
