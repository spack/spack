# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftSuite(BundlePackage):
    """BigDFT-suite: the complete suite of BigDFT for electronic structure calculation
    based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2")
    version("1.9.1")
    version("1.9.0")

    depends_on("python@3.0:", type=("run"))

    for vers in ["1.9.0", "1.9.1", "1.9.2", "develop"]:
        depends_on(f"bigdft-futile@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-psolver@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-libabinit@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-chess@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-core@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-spred@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-atlab@{vers}", when=f"@{vers}")
        depends_on(f"py-bigdft@{vers}", when=f"@{vers}")
