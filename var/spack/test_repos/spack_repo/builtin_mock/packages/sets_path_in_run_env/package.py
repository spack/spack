# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SetsPathInRunEnv(Package):
    """Package that sets a prefix-based path env var in setup_run_environment.

    Used to test that view path projection does not remap env vars for specs
    that are excluded from the target view.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("SETS_PATH_IN_RUN_ENV_DIR", self.prefix.share.join("my-data"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
