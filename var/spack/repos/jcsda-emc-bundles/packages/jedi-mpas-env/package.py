# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediMpasEnv(BundlePackage):
    """Development environment for mpas-bundle"""

    homepage = "https://github.com/JCSDA/mpas-bundle"
    git = "https://github.com/JCSDA/mpas-bundle.git"

    maintainers = ["climbfuji", "srherbener"]

    version("1.0.0")

    depends_on("jedi-base-env", type="run")

    # Anything missing?

    # There is no need for install() since there is no code.
