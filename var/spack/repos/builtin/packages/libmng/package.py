# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
