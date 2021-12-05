# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyToml(PythonPackage):
    """A Python library for parsing and creating TOML configuration files.
    For more information on the TOML standard, see
    https://github.com/toml-lang/toml.git"""

    homepage = "https://github.com/uiri/toml.git"
    pypi = "toml/toml-0.10.2.tar.gz"

    version('0.10.2', sha256='b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f')
    version('0.10.0', sha256='229f81c57791a41d65e399fc06bf0848bab550a9dfd5ed66df18ce5f05e73d5c')
    version('0.9.3', sha256='633a90ecb1f5665b58f0c94153fcf519313ef53e1de0eac90929cd6b6a014235', deprecated=True)

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
