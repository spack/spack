# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Integration tests for Linux Landlock sandboxing in the new installer."""

import pytest

import spack.concretize
import spack.sandbox


def _has_sandbox() -> bool:
    try:
        spack.sandbox.get_sandbox()
        return True
    except OSError:
        return False


requires_sandbox = pytest.mark.skipif(
    not _has_sandbox(), reason="platform does not support sandboxing"
)


@requires_sandbox
def test_sandbox_blocks_write_and_read_outside_prefix(install_mockery, mock_fetch, mutable_config):
    """A successful install proves the sandbox denied writes and reads outside the prefix.

    The mock package raises RuntimeError if either a home-dir write or an /etc/hostname read
    succeeds, so a clean install means the sandbox correctly blocked both operations.
    """
    from spack.new_installer import PackageInstaller
    mutable_config.set("config:sandbox", {"enable": True, "allow_network": True})
    spec = spack.concretize.concretize_one("sandbox-escape-test")
    PackageInstaller([spec.package], explicit=True).install()
    assert spec.installed
