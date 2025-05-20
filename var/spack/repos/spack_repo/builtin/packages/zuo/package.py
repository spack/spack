# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Zuo(AutotoolsPackage):
    """A tiny Racket for scripting."""

    homepage = "https://github.com/racket/zuo"
    url = "https://github.com/racket/zuo/archive/refs/tags/v1.11.tar.gz"

    license("Apache-2.0 AND MIT", checked_by="Buldram")
    maintainers("Buldram")

    version("1.12", sha256="0c8a3a86365fb10961d9a1f536b1cd0d7fcdc2779af03236a340539966b33f86")
    version("1.11", sha256="8404bea8ecae4576f44dece7efcab69d94c8a30ec10ea186f86823d37e74694b")

    variant("big", default=False, description="Enable hygienic macro support")

    depends_on("c", type="build")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("ZUO_JOBS", str(make_jobs))

    def configure_args(self):
        return [*self.enable_or_disable("big")]
