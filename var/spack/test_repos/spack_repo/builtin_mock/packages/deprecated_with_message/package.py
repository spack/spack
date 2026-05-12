# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DeprecatedWithMessage(Package):
    """Package using the deprecated() directive with a custom msg= string."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/deprecated-with-message-1.0.tar.gz"

    version("2.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    deprecated("@:1", reason="cve", severity="high", msg="Please upgrade to 2.0.")
