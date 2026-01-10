# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class TriggerAndEffectDeps(Package):
    """Package used to see if triggers and effects for dependencies are emitted correctly."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-a-dependency-1.0.tar.gz"
    version("1.0", sha256="0000000000000000000000000000000000000000000000000000000000000000")
    variant("x", default=False, description="x")
    variant("y", default=False, description="y")

    with when("+x"):
        depends_on("pkg-a", type="link")
        depends_on("pkg-b", type="link")

    with when("+y"):
        depends_on("pkg-a", type="run")
        depends_on("pkg-b", type="run")
