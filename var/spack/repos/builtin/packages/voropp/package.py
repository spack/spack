##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Voropp(MakefilePackage):
    """Voro++ is a open source software library for the computation of the
    Voronoi diagram, a widely-used tessellation that has applications in many
    scientific fields."""

    homepage = "http://math.lbl.gov/voro++/about.html"

    # This url is wrong but it passes the test the ++ make the url parser fail,
    # the correct url is constructed by url_for_version that has to be used in
    # any case due to the difference between the package name and the url
    url      = "http://math.lbl.gov/voropp/download/dir/voropp-0.4.6.tar.gz"

    version('0.4.6', '2338b824c3b7b25590e18e8df5d68af9')

    def url_for_version(self, version):
        url = "http://math.lbl.gov/voro++/download/dir/voro++-{0}.tar.gz".format(  # noqa: E501
            str(version))
        return url

    def edit(self, spec, prefix):
        filter_file(r'CC=g\+\+',
                    'CC={0}'.format(self.compiler.cxx),
                    'config.mk')
        filter_file(r'PREFIX=/usr/local',
                    'PREFIX={0}'.format(self.prefix),
                    'config.mk')
