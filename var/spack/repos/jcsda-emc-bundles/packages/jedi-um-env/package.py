# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediUmEnv(BundlePackage):
    """Development environment for um-bundle"""

    # Note. Internal only, but this repo was being frozen
    # in May 2022 and won't be developed any further.
    homepage = "https://github.com/JCSDA-internal/um-bundle"
    git = "https://github.com/JCSDA-internal/um-bundle.git"

    maintainers("climbfuji", "srherbener")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    depends_on("ectrans", type="run")
    depends_on("fiat", type="run")
    depends_on("shumlib", type="run")

    # There is no need for install() since there is no code.
