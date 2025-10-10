# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropRequires(Package):
    version("1.0")
    requires("hdf5")
    requires("mpi", when="@1.0")
    requires("netcdf-c", when="@1.0")
    drop_requires("hdf5")
    drop_requires("netcdf-c", when="@1.0")
