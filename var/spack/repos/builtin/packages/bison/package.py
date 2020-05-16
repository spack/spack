# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version
import sys


class Bison(AutotoolsPackage, GNUMirrorPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "https://www.gnu.org/software/bison/"
    gnu_mirror_path = "bison/bison-3.4.2.tar.gz"

    version('3.4.2', sha256='ff3922af377d514eca302a6662d470e857bd1a591e96a2050500df5a9d59facf')
    version('3.4.1', sha256='7007fc89c216fbfaff5525359b02a7e5b612694df5168c74673f67055f015095')
    version('3.3.2', sha256='0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1')
    version('3.0.5', sha256='cd399d2bee33afa712bac4b1f4434e20379e9b4099bce47189e09a7675a2d566')
    version('3.0.4', sha256='b67fd2daae7a64b5ba862c66c07c1addb9e6b1b05c5f2049392cfd8a2172952e')
    version('2.7',   sha256='19bbe7374fd602f7a6654c131c21a15aebdc06cc89493e8ff250cb7f9ed0a831')

    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    patch('parallel.patch', when='@3.4.2')

    depends_on('diffutils', type='build')
    depends_on('m4', type=('build', 'run'))
    depends_on('perl', type='build')
    depends_on('help2man', type='build')

    patch('pgi.patch', when='@3.0.4')

    conflicts('%intel@:14', when='@3.4.2:',
              msg="Intel 14 has immature C11 support")

    if sys.platform == 'darwin' and macos_version() >= Version('10.13'):
        patch('secure_snprintf.patch', level=0, when='@3.0.4')

    build_directory = 'spack-build'
