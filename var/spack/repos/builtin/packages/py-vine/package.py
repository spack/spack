# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVine(PythonPackage):
    """Promises, promises, promises."""

    homepage = "https://pypi.org/project/vine/"
    url      = "https://pypi.io/packages/source/v/vine/vine-1.2.0.tar.gz"

    version('1.3.0', sha256='133ee6d7a9016f177ddeaf191c1f58421a1dcc6ee9a42c58b34bed40e1d2cd87')
    version('1.2.0', sha256='ee4813e915d0e1a54e5c1963fde0855337f82655678540a6bc5996bca4165f76')

    depends_on('py-setuptools', type='build')
