# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedTool(Package):
    """A build tool whose old version is deprecated."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-tool-1.0.tar.gz"

    tags = ["build-tools"]

    version("2.0", md5="0123456789abcdef0123456789abcdef")
    version("1.0", md5="fedcba9876543210fedcba9876543210")

    deprecated("@1.0", reason="vuln", severity="critical")
