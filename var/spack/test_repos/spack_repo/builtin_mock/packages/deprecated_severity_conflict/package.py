# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedSeverityConflict(Package):
    """Package where higher version has higher deprecation severity.

    Without a severity-aware criterion, @2.0 (higher version) would be preferred.
    With the severity criterion at priority 315, @1.0 (lower severity) should win.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-severity-conflict-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    # @2.0 is deprecated at CRITICAL severity — solver should avoid it strongly
    deprecated("@2.0", reason="cve", severity="critical")
    # @1.0 is deprecated at LOW severity — acceptable penalty
    deprecated("@1.0", reason="rename", severity="low")
