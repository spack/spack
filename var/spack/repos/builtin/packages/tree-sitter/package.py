# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class TreeSitter(MakefilePackage):
    """Tree-sitter is a parser generator tool and an incremental parsing library.
    It can build a concrete syntax tree for a source file and
    efficiently update the syntax tree as the source file is edited."""

    homepage = "https://tree-sitter.github.io/tree-sitter/"
    url      = "https://github.com/tree-sitter/tree-sitter/archive/refs/tags/v0.20.1.tar.gz"

    maintainers = ['albestro']

    version('0.20.1', sha256='12a3f7206af3028dbe8a0de50d8ebd6d7010bf762db918acae76fc7585f1258d')

    def edit(self, spec, prefix):
        env['PREFIX'] = prefix
