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

    version("develop")

    variant(
        "debug",
        default=False,
        description="Build a debug version of certain dependencies (ESMF, MAPL)",
    )
    variant("python", default=True, description="Build Python dependencies")
    variant("shared", default=True, description="Build dynamic libraries when possible")

    depends_on("ufs-pyenv", type="run", when="+python")

    depends_on("bacio@2.4.1")
    depends_on("fms@2022.01")
    depends_on("crtm@2.4.0")
    depends_on("g2@3.4.5")
    depends_on("g2tmpl@1.10.0")
    depends_on("ip@3.3.3")
    depends_on("sp@2.3.3")
    depends_on("w3emc@2.9.2")

    depends_on("hdf5@1.10.6~shared+mpi~tools~threadsafe~cxx+hl", when="~shared")
    depends_on("jasper@2.0.25~shared", when="~shared")
    depends_on("libjpeg-turbo@2.1.0~shared", when="~shared")
    depends_on("libpng@1.6.37~shared", when="~shared")
    depends_on("netcdf-c@4.7.4~shared~parallel-netcdf~cdf5~dap~doxygen~parallel-tests~utilities+v2~largefile+mpi", when="~shared")
    depends_on("netcdf-fortran@4.5.4~shared", when="~shared")
    depends_on("zlib@1.2.11~shared", when="~shared")
    depends_on("parallelio@2.5.7+fortran~ipo~pnetcdf~shared", when="~shared")

    depends_on("hdf5@1.10.6+shared+mpi~tools~threadsafe~cxx+hl", when="+shared")
    depends_on("jasper@2.0.25+shared", when="+shared")
    depends_on("libjpeg-turbo@2.1.0+shared", when="+shared")
    depends_on("libpng@1.6.37+shared", when="+shared")
    depends_on("netcdf-c@4.7.4+shared~parallel-netcdf~cdf5~dap~doxygen~parallel-tests~utilities+v2~largefile+mpi", when="+shared")
    depends_on("netcdf-fortran@4.5.4+shared", when="+shared")
    depends_on("zlib@1.2.11+shared", when="+shared")
    depends_on("parallelio@2.5.7+fortran~ipo~pnetcdf+shared", when="+shared")

    esmf_ver = "8.3.0b09"
    depends_on(f"esmf@{esmf_ver}~debug+caplinks", when="~debug")
    depends_on(f"esmf@{esmf_ver}+debug+caplinks", when="+debug")
    mapl_ver = "2.22.0"
    depends_on(f"mapl@{mapl_ver}~debug~shared~pnetcdf~buildexe", type="run", when="~debug~shared")
    depends_on(f"mapl@{mapl_ver}~debug+shared~pnetcdf~buildexe", type="run", when="~debug+shared")
    depends_on(f"mapl@{mapl_ver}+debug", when="+debug")
