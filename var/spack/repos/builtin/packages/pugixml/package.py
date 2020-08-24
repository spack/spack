# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pugixml(CMakePackage):
    """Light-weight, simple, and fast XML parser for C++ with XPath support"""

    homepage = "http://pugixml.org/"
    url      = "https://github.com/zeux/pugixml/releases/download/v1.10/pugixml-1.10.tar.gz"

    version('1.8.1', sha256='929c4657c207260f8cc28e5b788b7499dffdba60d83d59f55ea33d873d729cd4')
    version('1.10', sha256='55f399fbb470942410d348584dc953bcaec926415d3462f471ef350f29b5870a')

    variant('shared', default=True, description='Enable shared libraries')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_AND_STATIC_LIBS:BOOL=OFF',
            '-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON',
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in self.spec else 'OFF')]

        return args
