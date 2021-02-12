# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBlessings(PythonPackage):
    """A nicer, kinder way to write to the terminal """
    homepage = "https://github.com/erikrose/blessings"
    pypi = "blessings/blessings-1.6.tar.gz"

    version('1.7',   sha256='98e5854d805f50a5b58ac2333411b0482516a8210f23f43308baeb58d77c157d')
    version('1.6.1', sha256='74919575885552e14bc24a68f8b539690bd1b5629180faa830b1a25b8c7fb6ea')
    version('1.6', sha256='edc5713061f10966048bf6b40d9a514b381e0ba849c64e034c4ef6c1847d3007')

    depends_on('py-setuptools', type='build')
