# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class I2(Package):
    version("1.0")

    provides("v1")

    variant("i2var", default=True)

    depends_on("p3")
    depends_on("p4")
