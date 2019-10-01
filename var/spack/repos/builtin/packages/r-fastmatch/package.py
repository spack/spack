# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFastmatch(RPackage):
    """Package providing a fast match() replacement for cases that require
       repeated look-ups. It is slightly faster that R's built-in match()
       function on first match against a table, but extremely fast on any
       subsequent lookup as it keeps the hash table in memory."""

    homepage = "http://www.rforge.net/fastmatch"
    url      = "https://cloud.r-project.org/src/contrib/fastmatch_1.1-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fastmatch"

    version('1.1-0', '900c2363c15059ac9d63c4c71ea2d6b2')
