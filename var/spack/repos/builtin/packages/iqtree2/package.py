# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Iqtree2(CMakePackage):
    """Efficient and versatile phylogenomic software by maximum likelihood"""

    homepage = "http://www.iqtree.org"
    url = "https://github.com/iqtree/iqtree2/archive/refs/tags/v2.1.2.tar.gz"

    version("2.1.2", sha256="3aaf5ac7f60d852ac8b733fb82832c049ca48b7203a6a865e99c5af359fcca5a")

    depends_on("boost", type="link")
    depends_on("eigen", type="link")
    depends_on("zlib", type="link")
