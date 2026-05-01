# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedWithReason(Package):
    """Package using the deprecated() directive with reason and severity metadata."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-reason-1.0.tar.gz"

    version("3.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    # @1.0 is deprecated with a CVE at high severity
    deprecated("@1.0", reason="cve", severity="high")
    # @2 is deprecated due to rename at low severity
    deprecated("@2", reason="rename", severity="low")
