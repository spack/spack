# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5netcdf(PythonPackage):
    """A Python interface for the netCDF4 file-format that reads and writes local or
    remote HDF5 files directly via h5py or h5pyd, without relying on the Unidata netCDF
    library."""

    homepage = "https://github.com/h5netcdf/h5netcdf"
    pypi = "h5netcdf/h5netcdf-0.10.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.3.0",
        sha256="f2df69dcd3665dc9c4d43eb6529dedd113b2508090d12ac973573305a8406465",
        url="https://pypi.org/packages/68/2d/63851081b19d1ccf245091255797cb358c53c886609b5056da5457f7dbbf/h5netcdf-1.3.0-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="2c526715f9010f403b7f667a146950515e44b17068196c3f004ee5c6c7563e18",
        url="https://pypi.org/packages/41/d4/ba3923cc4875e693d060b13ae53a8b3fee1588b11ddfb5b9247efaac2c97/h5netcdf-0.10.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@1.2:")
        depends_on("py-h5py")
        depends_on("py-packaging", when="@0.13.1:")
