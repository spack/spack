# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glfmultiples(MakefilePackage):
    """glfMultiples is a GLF-based variant caller for next-generation
       sequencing data. It takes a set of GLF format genotype likelihood
       files as input and generates a VCF-format set of variant calls
       as output. """

    homepage = "https://genome.sph.umich.edu/wiki/GlfMultiples"
    url      = "http://www.sph.umich.edu/csg/abecasis/downloads/generic-glfMultiples-2010-06-16.tar.gz"

    version('2010-06-16', '64bf6bb7c76543f4c8fabce015a3cb11')

    depends_on('zlib')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('CXX=.*', 'CXX = ' + env['CXX'])
        makefile.filter('CFLAGS=.*',
                        'CFLAGS=-O2 -I./libsrc -I./pdf ' +
                        '-D_FILE_OFFSET_BITS=64 -D__USE_LONG_INT')

    def install(self, spec, prefix):
        make('INSTALLDIR=%s' % prefix, 'install')
