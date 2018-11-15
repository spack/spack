# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jbigkit(MakefilePackage):
    """JBIG-Kit is a software implementation of
    the JBIG1 data compression standard."""

    homepage = "http://www.cl.cam.ac.uk/~mgk25/jbigkit/"
    url      = "http://www.cl.cam.ac.uk/~mgk25/jbigkit/download/jbigkit-2.1.tar.gz"

    version('2.1', 'ebcf09bed9f14d7fa188d3bd57349522')
    version('1.6', 'ce196e45f293d40ba76af3dc981ccfd7')

    build_directory = 'libjbig'

    def edit(self, spec, prefix):
        makefile = FileFilter('libjbig/Makefile')
        makefile.filter('CC = .*', 'CC = cc')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.include)
            for f in ['jbig85.h', 'jbig_ar.h', 'jbig.h']:
                install(f, prefix.include)
            mkdir(prefix.lib)
            for f in ['libjbig85.a', 'libjbig.a']:
                install(f, prefix.lib)
            mkdir(prefix.bin)
            for f in ['tstcodec', 'tstcodec85']:
                install(f, prefix.bin)
