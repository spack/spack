# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DeprecatedWithMessage(Package):
    """Package whose deprecated() directive includes guidance for the user."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-message-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@1.0", reason="retired", severity="high", msg="use @2.0, which is maintained")
