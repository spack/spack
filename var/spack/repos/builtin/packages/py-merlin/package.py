# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMerlin(PythonPackage):
    """A custom version of Phillip J. Eby's setuptools."""

    homepage = "https://pypi.org/project/merlin/"
    url      = "https://pypi.io/packages/source/m/merlin/merlin-1.8.tar.gz"

    version('1.8', sha256='a1ba9c13c74daa1724dd3820f1c241d7594d487b11f35347606986028c1881fd')

    depends_on('python@:2', type=('build', 'run'))

    def test(self):
        # Unit tests are missing from tarball
        pass
