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
import os


class Id3lib(AutotoolsPackage):
    """Library for manipulating ID3v1 and ID3v2 tags"""

    homepage = "http://id3lib.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/id3lib/id3lib/3.8.3/id3lib-3.8.3.tar.gz"

    version('3.8.3', '19f27ddd2dda4b2d26a559a4f0f402a7')

    def url_for_version(self, version):
        return 'https://downloads.sourceforge.net/project/id3lib/id3lib/{0}/id3lib-{0}.tar.gz'.format(version)

    depends_on('zlib')

    # http://connie.slackware.com/~alien/slackbuilds/id3lib/build/id3lib-3.8.3_gcc4.diff
    # this is due to some changes in the c++ standard library headers
    patch("id3lib-3.8.3_gcc4.diff")

    def configure_args(self):
        args = ["--enable-debug=no"]
        return args

    def install(self, spec, prefix):
        os.environ["LDFLAGS"] = " -lstdc++"
        make()
        make("install")
