# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsWeatherModelEnv(BundlePackage):
    """Development environment for ufs-weathermodel-bundle"""

    homepage = "https://github.com/ufs-community/ufs-weather-model"
    git = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers = ["AlexanderRichert-NOAA", "climbfuji"]

    version("1.0.0")

    variant(
        "debug",
        default=False,
        description="Build a debug version of certain dependencies (ESMF, MAPL)",
    )
    variant("python", default=True, description="Build Python dependencies")

    depends_on("base-env", type="run")
    depends_on("ufs-pyenv", type="run", when="+python")

    depends_on("fms@2022.01", type="run")
    depends_on("bacio", type="run")
    depends_on("crtm@2.4.0", type="run")
    depends_on("g2", type="run")
    depends_on("g2tmpl", type="run")
    depends_on("ip", type="run")
    depends_on("sp", type="run")
    depends_on("w3nco", type="run")

    depends_on("esmf~debug", type="run", when="~debug")
    depends_on("esmf+debug", type="run", when="+debug")
    depends_on("mapl~debug", type="run", when="~debug")
    depends_on("mapl+debug", type="run", when="+debug")

    # There is no need for install() since there is no code.
