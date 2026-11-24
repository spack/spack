# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class P1(Package):
    version("1.0")

    variant("p1var", default=True)
    variant("usev1", default=True)

    depends_on("p2")
    depends_on("v1", when="+usev1")
