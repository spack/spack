# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Nemsiogfs(CMakePackage):
    """
    Performs I/O for the NEMS-GFS model.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs/archive/refs/tags/v2.5.3.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs"

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett")

    version("develop", branch="develop")
    version("2.5.4", sha256="212f3ccde54590940d4fd7b486f4a7f9509ad89a0b19d6903501264203bcba80")
    version("2.5.3", sha256="bf84206b08c8779787bef33e4aba18404df05f8b2fdd20fc40b3af608ae4b9af")

    depends_on("fortran", type="build")

    depends_on("nemsio")

    conflicts("%oneapi", when="@:2.5.3")

    def check(self):
        with working_dir(self.build_directory):
            make("test")
