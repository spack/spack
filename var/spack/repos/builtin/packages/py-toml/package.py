# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyToml(PythonPackage):
    """A Python library for parsing and creating TOML configuration files.
    For more information on the TOML standard, see
    https://github.com/toml-lang/toml.git"""

    homepage = "https://github.com/uiri/toml.git"
    url      = "https://github.com/uiri/toml/archive/0.9.3.tar.gz"

    version('0.9.3', '58e3023a17509dcf4f50581bfc70ff23')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))

    phases = ['build', 'check', 'install']
