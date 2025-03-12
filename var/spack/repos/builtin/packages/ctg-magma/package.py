# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CtgMagma(MakefilePackage):
    """MAGMA is a tool for gene analysis and generalized gene-set analysis of GWAS data."""

    homepage = "https://cncr.nl/research/magma/"
    url = "https://vu.data.surfsara.nl/index.php/s/1OOi7bxLWef0GwY/download"

    license("GPL-3.0-only")

    version(
        "1.10", 
        url="https://vu.data.surfsara.nl/index.php/s/1OOi7bxLWef0GwY/download",
        sha256="c744c662204e6888f007b1db2c54d608545f2e71a73e5b42bf43102597c178af",
        extension="zip",
    )

    def install(self, spec, prefix):
        makedirs(prefix.bin)
        install("magma", prefix.bin.magma)
