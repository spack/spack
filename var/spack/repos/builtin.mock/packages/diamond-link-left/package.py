# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DiamondLinkLeft(Package):
    """Part of diamond-link-{top,left,right,bottom} group"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/diamond-link-left-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("diamond-link-bottom", type="link")
