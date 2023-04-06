# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class CrtmFix(Package):
    """CRTM coefficient files"""

    homepage = "https://github.com/NOAA-EMC/crtm"
    url = "ftp://ftp.ssec.wisc.edu/pub/s4/CRTM/fix_REL-2.3.0_emc.tgz"

    maintainers(
        "BenjaminTJohnson", "edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA", "climbfuji"
    )

    version("2.4.0_emc", sha256="88d659ae5bc4434f7fafa232ff65b4c48442d2d1a25f8fc96078094fa572ac1a")
    version("2.3.0_emc", sha256="1452af2d1d11d57ef3c57b6b861646541e7042a9b0f3c230f9a82854d7e90924")

    variant("big_endian", default=True, description="Install big_endian fix files")
    variant("little_endian", default=False, description="Install little endian fix files")
    variant("netcdf", default=True, description="Install netcdf fix files")

    conflicts("+big_endian", when="+little_endian", msg="big_endian and little_endian conflict")

    def url_for_version(self, version):
        url = "ftp://ftp.ssec.wisc.edu/pub/s4/CRTM/fix_REL-{}.tgz"
        return url.format(version)

    def install(self, spec, prefix):
        spec = self.spec
        mkdir(self.prefix.fix)

        endian_dirs = []
        if "+big_endian" in spec:
            endian_dirs.append("Big_Endian")
        elif "+little_endian" in spec:
            endian_dirs.append("Little_Endian")

        if "+netcdf" in spec:
            endian_dirs.extend(["netcdf", "netCDF"])

        fix_files = []
        for d in endian_dirs:
            fix_files = fix_files + find(".", "*/{}/*".format(d))

        # Big_Endian amsua_metop-c.SpcCoeff.bin is incorrect
        # Little_Endian amsua_metop-c_v2.SpcCoeff.bin is what it's supposed to be.
        # Remove the incorrect file, and install it as noACC,, then install
        # correct file under new name.
        if "+big_endian" in spec and spec.version == Version("2.4.0_emc"):
            remove_path = join_path(
                os.getcwd(), "fix", "SpcCoeff", "Big_Endian", "amsua_metop-c.SpcCoeff.bin"
            )
            fix_files.remove(remove_path)

            # This file is incorrect, install it as a different name.
            install(
                join_path("fix", "SpcCoeff", "Big_Endian", "amsua_metop-c.SpcCoeff.bin"),
                join_path(self.prefix.fix, "amsua_metop-c.SpcCoeff.noACC.bin"),
            )

            # This "Little_Endian" file is actually the correct one.
            install(
                join_path("fix", "SpcCoeff", "Little_Endian", "amsua_metop-c_v2.SpcCoeff.bin"),
                join_path(self.prefix.fix, "amsua_metop-c.SpcCoeff.bin"),
            )

        for f in fix_files:
            install(f, self.prefix.fix)

    def setup_run_environment(self, env):
        env.set("CRTM_FIX", self.prefix.fix)
