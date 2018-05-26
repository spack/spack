##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
