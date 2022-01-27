# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RViridislite(RPackage):
    """viridisLite: Default Color Maps from 'matplotlib' (Lite Version)"""

    homepage = "https://github.com/sjmgarnier/viridisLite"
    cran = "viridisLite"

    version(
        "0.4.0",
        sha256="849955dc8ad9bc52bdc50ed4867fd92a510696fc8294e6971efa018437c83c6a",
    )
    version(
        "0.3.0",
        sha256="780ea12e7c4024d5ba9029f3a107321c74b8d6d9165262f6e64b79e00aa0c2af",
    )
    version(
        "0.2.0",
        sha256="2d4d909f21c51e720bd685f05041ba158294e0a4064e0946d0bd916709818694",
    )

    depends_on("r@2.10:", type=("build", "run"))
