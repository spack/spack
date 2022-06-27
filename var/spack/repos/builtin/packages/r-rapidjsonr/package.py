# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRapidjsonr(RPackage):
    """'Rapidjson' C++ Header Files.

    Provides JSON parsing capability through the 'Rapidjson' 'C++' header-only
    library."""

    cran = "rapidjsonr"

    version('1.2.0', sha256='62c94fcdcf5d0fbdfa2f6168affe526bf547c37c16d94e2e1b78d7bf608eed1f')

    depends_on('gmake', type='build')
