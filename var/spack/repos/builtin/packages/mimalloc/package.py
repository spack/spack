# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mimalloc(CMakePackage):
    """mimalloc is a compact general purpose allocator with excellent performance."""

    homepage = "https://microsoft.github.io/mimalloc"
    url = "https://github.com/microsoft/mimalloc/archive/v0.0.0.tar.gz"
    maintainers = ['msimberg']

    version('dev-slice', git='https://github.com/microsoft/mimalloc.git', branch='dev-slice')
    version('dev', git='https://github.com/microsoft/mimalloc.git', branch='dev')
    version('master', git='https://github.com/microsoft/mimalloc.git', branch='master')
    version('2.0.6', sha256='9f05c94cc2b017ed13698834ac2a3567b6339a8bde27640df5a1581d49d05ce5')
    version('1.7.6', sha256='d74f86ada2329016068bc5a243268f1f555edd620b6a7d6ce89295e7d6cf18da')

    depends_on('cmake@3.0:', type='build')
