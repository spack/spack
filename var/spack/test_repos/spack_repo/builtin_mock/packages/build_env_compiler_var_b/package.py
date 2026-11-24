# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class BuildEnvCompilerVarB(Package):
    """Package with runtime variable that should be dropped in the parent's build environment."""

    url = "https://www.example.com"
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("CC", "this-should-be-dropped")
        env.set("CXX", "this-should-be-dropped")
        env.set("FC", "this-should-be-dropped")
        env.set("F77", "this-should-be-dropped")
        env.set("ANOTHER_VAR", "this-should-be-present")
