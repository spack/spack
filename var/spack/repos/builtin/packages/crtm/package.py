# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    depends_on("cmake@3.15:")
    depends_on("git-lfs")
    depends_on("netcdf-fortran", when="@2.4.0:")
    depends_on("netcdf-fortran", when="@v2.3-jedi.4")
    depends_on("netcdf-fortran", when="@v2.4-jedi.1")
    depends_on("netcdf-fortran", when="@v2.4-jedi.2")
    depends_on("netcdf-fortran", when="@v2.4.1-jedi")

    depends_on("crtm-fix@2.3.0_emc", when="@2.3.0 +fix")
    depends_on("crtm-fix@2.4.0_emc", when="@2.4.0 +fix")

    depends_on("ecbuild", type=("build"), when="@v2.3-jedi.4")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.1")
    depends_on("ecbuild", type=("build"), when="@v2.4-jedi.2")
    depends_on("ecbuild", type=("build"), when="@v2.4.1-jedi")

    # ecbuild release v2.4.0 is broken
    # add ecbuild dependency for next release with fix
    # depends_on("ecbuild", when="@2.4.0:", type=("build"))

    license("CC0-1.0")

    version(
        "v2.4.1-jedi", sha256="fd8bf4db4f2a3b420b4186de84483ba2a36660519dffcb1e0ff14bfe8c6f6a14"
    )
    version("2.4.0.1", tag="v2.4.0_emc.3", commit="7ecad4866c400d7d0db1413348ee225cfa99ff36")
    # REL-2.4.0_emc (v2.4.0 ecbuild does not work)
    version("2.4.0", commit="5ddd0d6b0138284764065feda73b5adf599082a2")
    # Uses the tip of REL-2.3.0_emc branch
    version("2.3.0", commit="99760e693ce3b90a3b3b0e97d80972b4dfb61196")
    # JEDI applications so far use these versions
    # Branch release/crtm_jedi
    version("v2.3-jedi.4", commit="bfede42adc6149213f28f58bf4e02fa8f7cb0198")
    # Branch release/crtm_jedi_v2.4.0
    version("v2.4-jedi.1", commit="82223419fdb479d76c2f2109c2b704e1d9618f22")
    version("v2.4-jedi.2", commit="62831cbb6c1ffcbb219eeec60e1b1c422526f597")

    def url_for_version(self, version):
        if self.spec.satisfies("@v3") or version >= Version("3.0.0"):
            return "https://github.com/JCSDA/crtmv3/archive/refs/tags/{}.tar.gz".format(version)
        else:
            return "https://github.com/JCSDA/crtm/archive/refs/tags/{}.tar.gz".format(version)

    @when("@2.4.0.1")
    def patch(self):
        if self.compiler.name in ["gcc", "clang", "apple-clang"]:
            # Line lengths in RSS_Emissivity_Model.f90 are too long for gfortran default limit
            filter_file(
                "-fbacktrace", "-fbacktrace -ffree-line-length-none", "libsrc/CMakeLists.txt"
            )
