# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CtgMagma(MakefilePackage):
    """MAGMA is a tool for gene analysis and generalized gene-set analysis of GWAS data."""

    homepage = "https://cncr.nl/research/magma/"
    url = "https://vu.data.surfsara.nl/index.php/s/1OOi7bxLWef0GwY/download"

    license("GPL-3.0-only")

    variant("bundled-deps", default=False, description="Use bundled versions of eigen and boost")

    with when("~bundled-deps"):
        depends_on("eigen")
        depends_on("boost@1.74:1.81+math+random")  # Boost::math requires C++14 after v1.82

    version(
        "1.10",
        url="https://vu.data.surfsara.nl/index.php/s/1OOi7bxLWef0GwY/download",
        sha256="c744c662204e6888f007b1db2c54d608545f2e71a73e5b42bf43102597c178af",
        extension="zip",
    )

    def patch(self):
        if self.spec.satisfies("~bundled-deps"):
            filter_file(
                "CXX_FLAGS += -I src/eigen -I src/boost/boost_1_74_0", "", "makefile", string=True
            )

    def install(self, spec, prefix):
        makedirs(prefix.bin)
        install("magma", prefix.bin.magma)
