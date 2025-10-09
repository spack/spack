# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropDependsOn(Package):
    version("1.0")
    depends_on("hdf5")
    depends_on("mpi", when="@1.0")
    depends_on("netcdf-c", when="@2")
    drop_depends_on("hdf5")
    drop_depends_on("netcdf-c", when="@1:")