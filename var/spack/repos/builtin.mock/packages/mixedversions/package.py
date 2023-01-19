# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mixedversions(Package):
    url = "http://www.fake-mixedversions.org/downloads/mixedversions-1.0.tar.gz"

    version("2.0.1", "0000000000000000000000000000000c")
    version("2.0", "0000000000000000000000000000000b")
    version("1.0.1", "0000000000000000000000000000000a")
