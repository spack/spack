# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropAllRequires(Package):
    version("1.0")
    requires("%gcc", when="@1.0")
    requires("%clang")
    drop_all_conflicts()