# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pugixml(CMakePackage):
    """Light-weight, simple, and fast XML parser for C++ with XPath support"""

    homepage = "http://pugixml.org/"
    url      = "http://github.com/zeux/pugixml/tarball/v1.8.1"

    version('1.8.1', 'bff935f82fa45bee4d31257d948bcba2')
