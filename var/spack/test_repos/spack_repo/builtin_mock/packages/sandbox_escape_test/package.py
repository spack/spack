# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SandboxEscapeTest(Package):
    """Verifies that write and read outside the install prefix are denied by the sandbox."""

    homepage = "http://www.example.com"
    url = "http://www.unit-test-should-replace-this-url/sandbox_escape_test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        # The home dir should not be writable.
        escape_write = os.path.join(os.path.expanduser("~"), ".spack_sandbox_escape")
        try:
            os.mkdir(escape_write)
            raise RuntimeError(f"Sandbox did not block write to {escape_write}")
        except PermissionError:
            pass

        # The /etc dir should not be readable.
        try:
            os.listdir("/etc")
            raise RuntimeError("Sandbox did not block read of /etc")
        except PermissionError:
            pass

        # Writing to the prefix should succeed
        touch(join_path(prefix, "sandbox_verified"))
