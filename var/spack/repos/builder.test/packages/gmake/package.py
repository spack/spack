# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmake(Package):
    """Gmake package"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/gmake-1.0.tar.gz"
    has_code = False

    version("1.0")
