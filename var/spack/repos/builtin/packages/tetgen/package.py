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
import glob


class Tetgen(Package):
    """TetGen is a program and library that can be used to generate
       tetrahedral meshes for given 3D polyhedral domains. TetGen
       generates exact constrained Delaunay tetrahedralizations,
       boundary conforming Delaunay meshes, and Voronoi paritions.
    """

    homepage = "http://wias-berlin.de/software/tetgen/"

    version('1.5.0', '3b9fd9cdec121e52527b0308f7aad5c1', url='http://www.tetgen.org/1.5/src/tetgen1.5.0.tar.gz')
    version('1.4.3', 'd6a4bcdde2ac804f7ec66c29dcb63c18', url='http://www.tetgen.org/files/tetgen1.4.3.tar.gz')

    variant('debug', default=False, description='Builds the library in debug mode.')
    variant('except', default=False, description='Replaces asserts with exceptions for better C++ compatibility.')

    patch('tetgen-1.5.0-free.patch', when='@1.5.0')

    def patch(self):
        cflags = '-g -O0' if '+debug' in self.spec else '-g0 -O3'

        mff = FileFilter('makefile')
        mff.filter(r'^(C(XX)?FLAGS\s*=)(.*)$', r'\1 {0}'.format(cflags))

        if '+except' in self.spec:
            hff = FileFilter('tetgen.h')
            hff.filter(r'(\b)(throw)(\b)(.*);', r'\1assert_throw(false);')
            hff.filter(r'^(#define\s*tetgenH\s*)$', r'\1{0}'.format("""\n
#include <stdexcept>

inline void assert_throw(bool assertion)
{
  if(!assertion)
    throw std::runtime_error("Tetgen encountered a problem (assert failed)!");
}\n"""))

            sff = FileFilter(*(glob.glob('*.cxx')))
            sff.filter(r'(\b)(assert)(\b)', r'\1assert_throw\3')

    def install(self, spec, prefix):
        make('tetgen', 'tetlib')

        mkdirp(prefix.bin)
        install('tetgen', prefix.bin)

        mkdirp(prefix.include)
        install('tetgen.h', prefix.include)

        mkdirp(prefix.lib)
        install('libtet.a', prefix.lib)
