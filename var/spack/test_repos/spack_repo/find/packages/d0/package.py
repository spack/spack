# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class D0(Package):
    version("1.2")
    version("1.1")

    depends_on("c0")
    depends_on("e0")
