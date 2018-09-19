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


class Libmng(AutotoolsPackage):
    """libmng -THE reference library for reading, displaying, writing
       and examining Multiple-Image Network Graphics.  MNG is the animation
       extension to the popular PNG image-format."""
    homepage = "http://sourceforge.net/projects/libmng/"
    url      = "http://downloads.sourceforge.net/project/libmng/libmng-devel/2.0.3/libmng-2.0.3.tar.gz"

    version('2.0.3', '7e9a12ba2a99dff7e736902ea07383d4')
    version('2.0.2', '1ffefaed4aac98475ee6267422cbca55')

    depends_on("jpeg")
    depends_on("zlib")
    depends_on("lcms")

    def patch(self):
        # jpeg requires stdio to be included before its headers.
        filter_file(r'^(\#include \<jpeglib\.h\>)',
                    '#include<stdio.h>\n\\1', 'libmng_types.h')

    @run_before('configure')
    def clean_configure_directory(self):
        """Without this, configure crashes with:

            configure: error: source directory already configured;
            run "make distclean" there first
        """
        make('distclean')
