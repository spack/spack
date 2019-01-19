# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version
import sys


class Bison(AutotoolsPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "http://www.gnu.org/software/bison/"
    url      = "https://ftpmirror.gnu.org/bison/bison-3.0.4.tar.gz"

    version('3.0.5', '41ad57813157b61bfa47e33067a9d6f0')
    version('3.0.4', 'a586e11cd4aff49c3ff6d3b6a4c9ccf8')
    version('2.7',   'ded660799e76fb1667d594de1f7a0da9')

    depends_on('diffutils', type='build')
    depends_on('m4', type=('build', 'run'))
    depends_on('perl', type='build')
    depends_on('help2man', type='build')

    patch('pgi.patch', when='@3.0.4')

    if sys.platform == 'darwin' and macos_version() >= Version('10.13'):
        patch('secure_snprintf.patch', level=0, when='@3.0.4')

    build_directory = 'spack-build'
