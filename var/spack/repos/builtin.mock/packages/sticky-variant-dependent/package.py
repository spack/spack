# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class StickyVariantDependent(AutotoolsPackage):
    """Package with a sticky variant and a conflict"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("sticky-variant")
    conflicts("%gcc", when="^sticky-variant~allow-gcc")

    depends_on("c", type="build")
