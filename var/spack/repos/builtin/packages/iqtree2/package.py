# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Iqtree2(CMakePackage):
    """Efficient and versatile phylogenomic software by maximum likelihood"""

    homepage = "http://www.iqtree.org"
    url = "https://github.com/iqtree/iqtree2/archive/refs/tags/v2.1.2.tar.gz"

    license("GPL-2.0-or-later")

    version("2.2.2.7", sha256="407a1a56d352ba9c2152a1d708cd29db872a41c252fbdc7acd8e0de0da8af008")
    version("2.2.2", sha256="2e9ce79427b140bca5f48b31fb098f394a21a7c5116bbbada1e3eabdd6efe982")
    version("2.1.2", sha256="3aaf5ac7f60d852ac8b733fb82832c049ca48b7203a6a865e99c5af359fcca5a")

    variant("lsd2", default=False, description="Build with LSD2 support")

    depends_on("boost", type="link")
    depends_on("eigen", type="link")
    depends_on("zlib-api", type="link")

    resource(
        name="lsd2-rsrc",
        url="https://github.com/tothuhien/lsd2/archive/refs/tags/v.2.4.1.tar.gz",
        sha256="3d0921c96edb8f30498dc8a27878a76d785516043fbede4a72eefd84b5955458",
        destination="lsd2-rsrc",
        when="+lsd2",
    )

    @run_before("cmake")
    def expand_resource(self):
        copy_tree(join_path("lsd2-rsrc", "*"), "lsd2")

    def cmake_cargs(self):
        args = [self.define_from_variant("USE_LSD2", variant="lsd2")]

        return args
