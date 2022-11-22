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
    variant("shared", default=True, description="Build dynamic libraries when possible")

    depends_on("ufs-pyenv", type="run", when="+python")

    depends_on("bacio")
    depends_on("fms@2022.01")
    depends_on("crtm@2.4.0")
    depends_on("g2")
    depends_on("g2tmpl")
    depends_on("ip")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("parallelio+fortran~pnetcdf~shared")

    depends_on("hdf5+hl+mpi~shared", when="~shared")
    depends_on("jasper~shared", when="~shared")
    depends_on("libjpeg-turbo~shared", when="~shared")
    depends_on("libpng~shared", when="~shared")
    depends_on("netcdf-c~parallel-netcdf+v2+mpi~shared", when="~shared")
    depends_on("netcdf-fortran~shared", when="~shared")
    depends_on("zlib~shared", when="~shared")
    depends_on("parallel-netcdf~shared", when="~shared")

    depends_on("hdf5+hl+mpi+shared", when="+shared")
    depends_on("jasper+shared", when="+shared")
    depends_on("libpng+shared", when="+shared")
    depends_on("netcdf-c~parallel-netcdf+v2+mpi+shared", when="+shared")
    depends_on("netcdf-fortran+shared", when="+shared")
    depends_on("zlib+shared", when="+shared")

    depends_on("esmf~debug", when="~debug")
    depends_on("esmf+debug", when="+debug")
    depends_on("mapl~pnetcdf~debug~shared", type="run", when="~debug~shared")
    depends_on("mapl~pnetcdf~debug+shared", type="run", when="~debug+shared")
    depends_on("mapl~pnetcdf+debug~shared", type="run", when="+debug~shared")
    depends_on("mapl~pnetcdf+debug+shared", type="run", when="+debug+shared")
