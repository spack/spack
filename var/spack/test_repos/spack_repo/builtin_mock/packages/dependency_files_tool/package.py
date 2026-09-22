# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class DependencyFilesTool(Package):
    """Package detected by its executable, which other packages run"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dependency-files-tool-2.0.tar.gz"

    executables = ["^dependency-files-tool$"]

    version("2.0", md5="0123456789abcdef0123456789abcdef")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)(output=str, error=str)
        match = re.search(r"dependency-files-tool (\S+)", output)
        return match.group(1) if match else None
