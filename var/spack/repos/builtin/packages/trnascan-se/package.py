# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TrnascanSe(AutotoolsPackage):
    """Seaching for tRNA genes in genomic sequence"""

    homepage = "http://lowelab.ucsc.edu/tRNAscan-SE/"
    url = "http://trna.ucsc.edu/software/trnascan-se-2.0.0.tar.gz"

    version("2.0.11", sha256="29b74edd0f84ad88139035e119b66397c54a37428e0b61c66a1b3d4733adcd1e")
    version("2.0.0", sha256="0dde1c07142e4bf77b21d53ddf3eeb1ef8c52248005a42323d13f8d7c798100c")

    depends_on("autoconf", type="build")
    depends_on("infernal@1.1:", type="run", when="@2.0.0:")

    def patch(self):
        filter_file(
            "infernal_dir: {bin_dir}",
            "infernal_dir: %s" % self.spec["infernal"].prefix.bin,
            "tRNAscan-SE.conf.src",
            string=True,
        )
