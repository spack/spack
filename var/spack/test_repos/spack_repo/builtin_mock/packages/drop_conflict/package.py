# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropConflict(Package):
    version("1.0")
    conflicts("%gcc", when="@1.0")
    conflicts("%clang")
    conflicts("^hdf5", when="@1.0")
    drop_conflict("%clang")
    drop_conflict("^hdf5", when="@1.0")
