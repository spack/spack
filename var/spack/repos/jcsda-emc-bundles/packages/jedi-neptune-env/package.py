# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediNeptuneEnv(BundlePackage):
    """Development environment for neptune-bundle"""

    # Fake URL
    homepage = "https://github.com/JCSDA-internal/neptune-bundle"
    git = "https://github.com/JCSDA-internal/neptune-bundle.git"

    maintainers("climbfuji", "areineke")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")

    depends_on("libyaml", type="run")
    depends_on("p4est", type="run")
    depends_on("w3emc", type="run")
    depends_on("w3nco", type="run")
    depends_on("esmf", type="run")
    depends_on("nco", type="run")

    # There is no need for install() since there is no code.
