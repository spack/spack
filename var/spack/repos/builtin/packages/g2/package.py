# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class G2(CMakePackage):
    """The NCEPLIBS-g2 library reads and writes GRIB2 files. GRIdded Binary or General
    Regularly-distributed Information in Binary form (GRIB) is a data format for
    meteorological and forecast data, standardized by the World Meteorological
    Organization (WMO).

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-g2"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-g2/archive/refs/tags/v3.4.3.tar.gz"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("3.4.6", sha256="c4b03946365ce0bacf1e10e8412a5debd72d8671d1696aa4fb3f3adb119175fe")
    version("3.4.5", sha256="c18e991c56964953d778632e2d74da13c4e78da35e8d04cb742a2ca4f52737b6")
    version("3.4.3", sha256="679ea99b225f08b168cbf10f4b29f529b5b011232f298a5442ce037ea84de17c")

    variant(
        "build_with_w3emc",
        description="Enable GRIB1 conversion routine",
        default=True,
        when="@3.4.5:",
    )

    depends_on("libpng")
    depends_on("bacio")
    depends_on("jasper@:2.0.32", when="@:3.4.5")
    depends_on("jasper", when="@3.4.6:")
    depends_on("w3emc", when="@:3.4.5")

    def cmake_args(self):
        args = []

        if self.spec.satisfies("@3.4.5:"):
            args.append(self.define_from_variant("BUILD_WITH_W3EMC", "build_with_w3emc"))

    def setup_run_environment(self, env):
        for suffix in ("4", "d"):
            lib = find_libraries("libg2_" + suffix, root=self.prefix, shared=False, recursive=True)
            env.set("G2_LIB" + suffix, lib[0])
            env.set("G2_INC" + suffix, join_path(self.prefix, "include_" + suffix))
