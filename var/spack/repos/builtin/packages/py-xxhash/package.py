# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXxhash(PythonPackage):
    """xxhash is a Python binding for the xxHash library by
    Yann Collet."""

    homepage = "https://github.com/ifduyue/python-xxhash"
    pypi     = "xxhash/xxhash-2.0.2.tar.gz"

    version('2.0.2', sha256='b7bead8cf6210eadf9cecf356e17af794f57c0939a3d420a00d87ea652f87b49')

    depends_on('python@2.6:2,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('xxhash@0.8.0')

    def setup_build_environment(self, env):
        env.set('XXHASH_LINK_SO', '1')
