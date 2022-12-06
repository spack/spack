# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediBaseEnv(BundlePackage):
    """Basic development environment for JEDI applications"""

    homepage = "https://github.com/noaa-emc/spack-stack"
    git = "https://github.com/noaa-emc/spack-stack.git"

    maintainers = ["climbfuji", "srherbener"]

    version("1.0.0")

    # Variants defining packages that we cannot distribute publicly
    # Need to find a free fftw provider for fftw-api ...
    variant("fftw", default=True, description="Build fftw")
    variant("hdf4", default=True, description="Build hdf4 library and python hdf module")
    variant("python", default=True, description="Build Python libraries")

    depends_on("base-env", type="run")
    depends_on("bison@3:", type="run")
    depends_on("blas", type="run")
    depends_on("boost", type="run")
    depends_on("bufr", type="run")
    depends_on("crtm@v2.4-jedi.1", type="run")
    depends_on("ecbuild", type="run")
    depends_on("eccodes", type="run")
    depends_on("eckit", type="run")
    depends_on("ecmwf-atlas", type="run")
    depends_on("eigen", type="run")
    depends_on("fckit", type="run")
    depends_on("fftw-api", when="+fftw", type="run")
    depends_on("flex", type="run")
    depends_on("git-lfs", type="run")
    depends_on("gsibec", type="run")
    depends_on("gsl-lite", type="run")
    depends_on("hdf", when="+hdf4", type="run")
    depends_on("jedi-cmake", type="run")
    depends_on("netcdf-cxx4", type="run")
    depends_on("ncview", type="run")
    depends_on("nlohmann-json", type="run")
    depends_on("nlohmann-json-schema-validator", type="run")
    depends_on("odc", type="run")
    depends_on("udunits", type="run")

    with when("+python"):
        depends_on("py-eccodes", type="run")
        depends_on("py-f90nml", type="run")
        depends_on("py-h5py", type="run")
        depends_on("py-netcdf4", type="run")
        depends_on("py-pandas", type="run")
        depends_on("py-pycodestyle", type="run")
        depends_on("py-pybind11", type="run")
        depends_on("py-pyhdf", when="+hdf4", type="run")
        depends_on("py-python-dateutil", type="run")
        depends_on("py-pyyaml", type="run")
        depends_on("py-scipy", type="run")
        depends_on("py-xarray", type="run")

    # There is no need for install() since there is no code.
