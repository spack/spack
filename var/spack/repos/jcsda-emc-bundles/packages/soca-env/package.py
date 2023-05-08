# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SocaEnv(BundlePackage):
    """Development environment for soca-bundle"""

    homepage = "https://github.com/JCSDA/soca"
    git = "https://github.com/JCSDA/soca.git"

    maintainers("climbfuji", "travissluka")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    depends_on("nco", type="run")

    # There is no need for install() since there is no code.
