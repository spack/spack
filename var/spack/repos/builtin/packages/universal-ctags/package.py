# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UniversalCtags(AutotoolsPackage):
    """Universal Ctags generates an index (or tag) file of language
    objects found in source files for many popular programming languages.
    This index makes it easy for text editors and other tools to locate
    the indexed items."""

    homepage = "https://ctags.io/"
    url      = "https://github.com/universal-ctags/ctags/archive/refs/tags/p5.9.20210808.0.tar.gz"
    git      = "https://github.com/universal-ctags/ctags.git"

    version('master', branch='master')
    version('5.9.20210808.0', sha256='7f5f88d20750dfa2437ca9d163972b8684e3cf16de022a5177f322be92f528cc')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libiconv', type='link')
    depends_on('pkg-config', type='build')
