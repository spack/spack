# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DeprecatedVersions(Package):
    """Package with the most recent version deprecated"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/c-1.0.tar.gz"

    version("1.1.0", md5="0123456789abcdef0123456789abcdef", deprecated=True)
    version("1.0.0", md5="0123456789abcdef0123456789abcdef")
