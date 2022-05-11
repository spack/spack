# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyringsAlt(PythonPackage):
    """Alternate keyring implementations"""

    homepage = "https://github.com/jaraco/keyrings.alt"
    pypi     = "keyrings.alt/keyrings.alt-4.0.2.tar.gz"

    version('4.1.0', sha256='52ccb61d6f16c10f32f30d38cceef7811ed48e086d73e3bae86f0854352c4ab2')
    version('4.0.2', sha256='cc475635099d6edd7e475c5a479e5b4da5e811a3af04495a1e9ada488d16fe25')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools-scm+toml@3.4.1:', type='build')
