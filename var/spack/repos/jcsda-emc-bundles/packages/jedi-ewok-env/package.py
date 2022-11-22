# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediEwokEnv(BundlePackage):
    """Development environment for ewok"""

    # DH* TODO UPDATE FROM INTERNAL TO PUBLIC
    homepage = "https://github.com/JCSDA-internal/ewok"
    git = "https://github.com/JCSDA-internal/ewok.git"

    maintainers = ["climbfuji", "ericlingerfelt"]

    version("1.0.0")

    # Variants defining repositories that are not yet publicly available
    variant("solo", default=False, description="Build solo (general tools for Python programmers)")
    variant(
        "r2d2",
        default=False,
        description="Build R2D2 (Research Repository for Data and Diagnostics)",
    )
    variant(
        "ewok",
        default=False,
        description="Build EWOK (Experiments and Workflows Orchestration Kit)",
    )

    depends_on("jedi-base-env +python", type="run")
    depends_on("py-boto3", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-jinja2", type="run")
    depends_on("py-ruamel-yaml", type="run")
    depends_on("py-ruamel-yaml-clib", type="run")
    depends_on("ecflow", type="run")

    depends_on("solo", when="+solo", type="run")
    depends_on("r2d2", when="+r2d2", type="run")
    depends_on("ewok", when="+ewok", type="run")

    conflicts(
        "%gcc platform=darwin",
        msg="jedi-ewok-env does " + "not build with gcc (11?) on macOS (12), use apple-clang",
    )

    # There is no need for install() since there is no code.
