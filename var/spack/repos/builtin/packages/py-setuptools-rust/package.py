# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PySetuptoolsRust(PythonPackage):
    """Setuptools rust extension plugin."""

    homepage = "https://github.com/PyO3/setuptools-rust"
    pypi = "setuptools-rust/setuptools-rust-0.12.1.tar.gz"

    version('0.12.1', sha256='647009e924f0ae439c7f3e0141a184a69ad247ecb9044c511dabde232d3d570e')

    # Version 0.10.6 is not available on pypi and can only be found on github
    version('0.10.6', sha256='1446d3985e4aaf4cc679fda8a48a73ac1390b627c8ae1bebe7d9e08bb3b33769',
            url="https://github.com/PyO3/setuptools-rust/archive/v0.10.6.tar.gz",
            deprecated=True)

    depends_on('python@3.6:', when='@0.12:', type=('build', 'run'))
    depends_on('py-setuptools@46.1:', when='@0.11.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm+toml@3.4.3:', when='@0.11:', type='build')
    depends_on('py-semantic-version@2.6.0:', type=('build', 'run'))
    depends_on('py-toml@0.9.0:', type=('build', 'run'))
    depends_on('rust', type='run')
