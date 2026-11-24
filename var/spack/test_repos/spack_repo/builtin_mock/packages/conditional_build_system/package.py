# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin_mock.build_systems.cmake import CMakePackage

from spack.package import *


class ConditionalBuildSystem(AutotoolsPackage, CMakePackage):
    """Package with two build systems, each available on a different range of versions.

    The default build system is available only on the most recent versions.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/conditional-build-system-1.0.tar.gz"

    version("2.0")
    version("1.0")

    build_system(
        conditional("mock_cmake", when="@2:"),
        conditional("mock_autotools", when="@:1"),
        default="mock_cmake",
    )

    variant(
        "flavor",
        default="new",
        values=(conditional("new", when="@2:"), conditional("old", when="@:1")),
        multi=False,
        description="Variant whose default value is not available on all versions",
    )

    variant(
        "static",
        default=False,
        description="Variant tied to the build system, and not to the version",
        when="build_system=mock_autotools",
    )
