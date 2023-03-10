# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class TreeSitter(MakefilePackage):
    """Tree-sitter is a parser generator tool and an incremental parsing library.
    It can build a concrete syntax tree for a source file and
    efficiently update the syntax tree as the source file is edited."""

    homepage = "https://tree-sitter.github.io/tree-sitter/"
    url = "https://github.com/tree-sitter/tree-sitter/archive/refs/tags/v0.20.1.tar.gz"

    maintainers("albestro")

    version("0.20.6", sha256="4d37eaef8a402a385998ff9aca3e1043b4a3bba899bceeff27a7178e1165b9de")
    version("0.20.4", sha256="979ad0b36eb90975baf0c65d155d106276cac08afb1c2fe0ad54d4b7d498ce39")
    version("0.20.3", sha256="ab52fe93e0c658cff656b9d10d67cdd29084247052964eba13ed6f0e9fa3bd36")
    version("0.20.2", sha256="2a0445f8172bbf83db005aedb4e893d394e2b7b33251badd3c94c2c5cc37c403")
    version("0.20.1", sha256="12a3f7206af3028dbe8a0de50d8ebd6d7010bf762db918acae76fc7585f1258d")

    def edit(self, spec, prefix):
        env["PREFIX"] = prefix
