# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class TreeSitter(MakefilePackage):
    """Tree-sitter is a parser generator tool and an incremental parsing library.
    It can build a concrete syntax tree for a source file and
    efficiently update the syntax tree as the source file is edited."""

    homepage = "https://tree-sitter.github.io/tree-sitter/"
    url = "https://github.com/tree-sitter/tree-sitter/archive/refs/tags/v0.20.1.tar.gz"

    maintainers("albestro")

    license("MIT")

    version("0.25.3", sha256="862fac52653bc7bc9d2cd0630483e6bdf3d02bcd23da956ca32663c4798a93e3")
    version("0.25.2", sha256="26791f69182192fef179cd58501c3226011158823557a86fe42682cb4a138523")
    version("0.25.1", sha256="99a2446075c2edf60e82755c48415d5f6e40f2d9aacb3423c6ca56809b70fe59")
    version("0.25.0", sha256="3729e98e54a41a4c03f4f6c0be580d14ed88c113d75acf15397b16e05cf91129")
    version("0.24.7", sha256="7cbc13c974d6abe978cafc9da12d1e79e07e365c42af75e43ec1b5cdc03ed447")
    version("0.24.6", sha256="03c7ee1e6f9f4f3821fd4af0ae06e1da60433b304a73ff92ee9694933009121a")
    version("0.24.5", sha256="b5ac48acf5a04fd82ccd4246ad46354d9c434be26c9606233917549711e4252c")
    version("0.24.4", sha256="d704832a6bfaac8b3cbca3b5d773cad613183ba8c04166638af2c6e5dfb9e2d2")
    version("0.24.3", sha256="0a8d0cf8e09caba22ed0d8439f7fa1e3d8453800038e43ccad1f34ef29537da1")
    version("0.24.2", sha256="199da041ac7ef62bccdda9b7bec28aafa073f7eea2677680aa7992d503c9cc64")
    version("0.22.6", sha256="e2b687f74358ab6404730b7fb1a1ced7ddb3780202d37595ecd7b20a8f41861f")
    version("0.22.5", sha256="6bc22ca7e0f81d77773462d922cf40b44bfd090d92abac75cb37dbae516c2417")
    version("0.22.4", sha256="919b750da9af1260cd989498bc84c63391b72ee2aa2ec20fc84882544eb7a229")
    version("0.22.3", sha256="b394b948646e67c81319f3b859a09b50280b16c66b4445ae1958b35aa4eed586")
    version("0.22.2", sha256="0c829523b876d4a37e1bd46a655c133a93669c0fe98fcd84972b168849c27afc")
    version("0.22.1", sha256="b21065e78da33e529893c954e712ad15d9ad44a594b74567321d4a3a007d6090")
    version("0.22.0", sha256="1cc0c832c6cc3d04f0b702247fac3dac45f958b0ee1f946619b7ae7b67258060")
    version("0.21.0", sha256="6bb60e5b63c1dc18aba57a9e7b3ea775b4f9ceec44cc35dac4634d26db4eb69c")
    version("0.20.9", sha256="9b2fd489a7281e3a7e5e7cbbf3a974e5a6a115889ae65676d61b79bdae96464e")
    version("0.20.8", sha256="6181ede0b7470bfca37e293e7d5dc1d16469b9485d13f13a605baec4a8b1f791")
    version("0.20.7", sha256="b355e968ec2d0241bbd96748e00a9038f83968f85d822ecb9940cbe4c42e182e")
    version("0.20.6", sha256="4d37eaef8a402a385998ff9aca3e1043b4a3bba899bceeff27a7178e1165b9de")
    version("0.20.4", sha256="979ad0b36eb90975baf0c65d155d106276cac08afb1c2fe0ad54d4b7d498ce39")
    version("0.20.3", sha256="ab52fe93e0c658cff656b9d10d67cdd29084247052964eba13ed6f0e9fa3bd36")
    version("0.20.2", sha256="2a0445f8172bbf83db005aedb4e893d394e2b7b33251badd3c94c2c5cc37c403")
    version("0.20.1", sha256="12a3f7206af3028dbe8a0de50d8ebd6d7010bf762db918acae76fc7585f1258d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def edit(self, spec, prefix):
        env["PREFIX"] = prefix

        # Starting from 0.25.0 endianness is taken into account using system headers
        #   https://github.com/tree-sitter/tree-sitter/pull/3740
        # but GLIBC provides them according to some defines that changed over time.
        #   https://www.sourceware.org/glibc/wiki/Release/2.20#Deprecation_of__BSD_SOURCE_and__SVID_SOURCE_feature_macros
        if spec.satisfies("@0.25: ^glibc@:2.19"):
            filter_file("-D_DEFAULT_SOURCE", "-D_BSD_SOURCE", "Makefile")
