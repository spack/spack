# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class RedistributeX(Package):
    version("1.3")
    version("1.2")
    version("1.1")
    version("1.0")

    variant("foo", default=False)

    redistribute(binary=False, when="@1.1")
    redistribute(binary=False, when="@1.0:1.2+foo")
    redistribute(source=False, when="@1.0:1.2")
