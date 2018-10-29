# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os.path


class Tinyxml(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml/"
    url = "https://downloads.sourceforge.net/project/tinyxml/tinyxml/2.6.2/tinyxml_2_6_2.tar.gz"

    version('2.6.2', 'cba3f50dd657cb1434674a03b21394df9913d764')

    variant('shared', default=True, description='Build a shared library')

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/tinyxml/files/tinyxml/{0}/tinyxml_{1}.tar.gz"
        return url.format(version.dotted, version.underscored)

    def patch(self):
        copy(join_path(os.path.dirname(__file__),
             "CMakeLists.txt"), "CMakeLists.txt")

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS=%s' % ('YES' if '+shared' in spec else 'NO')]
