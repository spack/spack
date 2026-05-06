# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class UsesDeprecatedReplace(Package):
    """Package that depends_on deprecated-with-replace with a deprecated variant (+shared)."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/uses-deprecated-replace-1.0.tar.gz"

    version("1.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")

    depends_on("deprecated-with-replace+shared")
