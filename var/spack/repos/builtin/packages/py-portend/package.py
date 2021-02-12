# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPortend(PythonPackage):
    """TCP port monitoring and discovery """

    homepage = "https://github.com/jaraco/portend"
    pypi = "portend/portend-2.5.tar.gz"

    version('2.7.0', sha256='ac0e57ae557f75dc47467579980af152e8f60bc2139547eff8469777d9110379')
    version('2.6',   sha256='600dd54175e17e9347e5f3d4217aa8bcf4bf4fa5ffbc4df034e5ec1ba7cdaff5')
    version(
        '2.5', sha256='19dc27bfb3c72471bd30a235a4d5fbefef8a7e31cab367744b5d87a205e7bfd9')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-tempora@1.8:', type=('run', 'build'))
    depends_on('python@2.7:', type=('run', 'build'))
