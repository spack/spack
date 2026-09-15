# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.makefile import MakefilePackage

from spack.package import *


class FailTestAuditWhenCallback(MakefilePackage):
    """Simple package combining @when with phase callback decorators."""

    homepage = "http://github.com/dummy/fail-test-audit-when-callback"
    url = "https://github.com/dummy/fail-test-audit-when-callback/archive/v1.0.tar.gz"

    version("1.0", sha256="abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234")

    @run_before("build")
    @when("@1.0:")
    def callback_outside(self):
        pass

    @when("@1.0:")
    @run_after("install")
    def callback_inside(self):
        pass
