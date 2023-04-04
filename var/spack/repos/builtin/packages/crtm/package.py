# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crtm(CMakePackage):
    """The Community Radiative Transfer Model (CRTM) package.
    The CRTM is composed of four important modules for gaseous transmittance,
    surface emission and reflection, cloud and aerosol absorption and
    scattering, and a solver for a radiative transfer."""

    homepage = "https://www.jcsda.org/jcsda-project-community-radiative-transfer-model"
    git = "https://github.com/JCSDA/crtm.git"
    url = "https://github.com/JCSDA/crtm/archive/refs/tags/v2.3.0.tar.gz"

    maintainers(
        "BenjaminTJohnson",
        "t-brown",
        "edwardhartnett",
        "AlexanderRichert-NOAA",
        "Hang-Lei-NOAA",
        "climbfuji",
    )

    variant(
        "fix", default=False, description='Download CRTM coeffecient or "fix" files (several GBs).'
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    depends_on("cmake@3.15:")
    depends_on("git-lfs")
    depends_on("netcdf-fortran", when="@2.4.0:")
    depends_on("netcdf-fortran", when="@v2.3-jedi.4")
    depends_on("netcdf-fortran", when="@v2.4-jedi.1")
    depends_on("netcdf-fortran", when="@v2.4-jedi.2")

    depends_on("crtm-fix@2.3.0_emc", when="@2.3.0 +fix")
    depends_on("crtm-fix@2.4.0_emc", when="@2.4.0 +fix")

    depends_on("ecbuild", type=("build"), when="@v2.3-jedi.4")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.1")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.2")

    # ecbuild release v2.4.0 is broken
    # add ecbuild dependency for next release with fix
    # depends_on("ecbuild", when="@2.4.0:", type=("build"))

    # REL-2.4.0_emc (v2.4.0 ecbuild does not work)
    version("2.4.0", commit="5ddd0d6")
    # Uses the tip of REL-2.3.0_emc branch
    version("2.3.0", commit="99760e6")
    # JEDI applications so far use these versions
    # Branch release/crtm_jedi
    version("v2.3-jedi.4", commit="bfede42")
    # Branch release/crtm_jedi_v2.4.0
    version("v2.4-jedi.1", commit="8222341")
    version("v2.4-jedi.2", commit="62831cb")
