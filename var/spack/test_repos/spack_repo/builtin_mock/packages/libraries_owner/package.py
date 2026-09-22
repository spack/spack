# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class LibrariesOwner(Package):
    """Package detected by its libraries"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/libraries-owner-1.0.tar.gz"

    # A prefix, as in many recipes: the version detection selects the files
    libraries = [r"^liblibraries-owner"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"liblibraries-owner\.so\.(\d+\.\d+)$", lib)
        return match.group(1) if match else None
