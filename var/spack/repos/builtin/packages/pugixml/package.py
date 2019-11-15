# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pugixml(CMakePackage):
    """Light-weight, simple, and fast XML parser for C++ with XPath support"""

    homepage = "http://pugixml.org/"
    url      = "http://github.com/zeux/pugixml/tarball/v1.8.1"

    version('1.9', 'cac3d11a62e391f834caa239e8b18b4e9ebc46c8c144403473665584044f1666')
    version('1.8.1', sha256='929c4657c207260f8cc28e5b788b7499dffdba60d83d59f55ea33d873d729cd4')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON'
        ]
        return args
