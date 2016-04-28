##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import glob, sys, os

class Metis(Package):
    """
    METIS is a set of serial programs for partitioning graphs, partitioning finite element meshes, and producing fill
    reducing orderings for sparse matrices. The algorithms implemented in METIS are based on the multilevel
    recursive-bisection, multilevel k-way, and multi-constraint partitioning schemes.
    """

    homepage = 'http://glaros.dtc.umn.edu/gkhome/metis/metis/overview'
    url = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe',
            url='http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz')
    version('4.0.3', '5efa35de80703c1b2c4d0de080fafbcf4e0d363a21149a1ad2f96e0144841a55',
            url='http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/OLD/metis-4.0.3.tar.gz')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds the library in debug mode')
    variant('gdb', default=False, description='Enables gdb support')

    variant('idx64', default=False, description='Use int64_t as default index type')
    variant('double', default=False, description='Use double precision floating point types')

    depends_on('cmake @2.8:', when='@5:')  # build-time dependency
    depends_on('gdb', when='+gdb')

    patch('install_gklib_defs_rename.patch', when='@5:')


    @when('@4:4.0.3')
    def install(self, spec, prefix):

        if '+gdb' in spec:
            raise InstallError('gdb support not implemented in METIS 4!')
        if '+idx64' in spec:
            raise InstallError('idx64 option not implemented in METIS 4!')
        if '+double' in spec:
            raise InstallError('double option not implemented for METIS 4!')

        options = ['COPTIONS=-fPIC']
        if '+debug' in spec:
            options.append('OPTFLAGS=-g -O0')
        make(*options)

        mkdir(prefix.bin)
        for x in ('pmetis', 'kmetis', 'oemetis', 'onmetis', 'partnmesh',
                  'partdmesh', 'mesh2nodal', 'mesh2dual', 'graphchk'):
            install(x, prefix.bin)

        mkdir(prefix.lib)
        install('libmetis.a', prefix.lib)

        mkdir(prefix.include)
        for h in glob.glob(join_path('Lib', '*.h')):
            install(h, prefix.include)

        mkdir(prefix.share)
        for f in (join_path(*p)
                  for p in (('Programs', 'io.c'),
                            ('Test','mtest.c'),
                            ('Graphs','4elt.graph'),
                            ('Graphs', 'metis.mesh'),
                            ('Graphs', 'test.mgraph'))):
            install(f, prefix.share)

        if '+shared' in spec:
            if sys.platform == 'darwin':
                lib_dsuffix = 'dylib'
                load_flag = '-Wl,-all_load'
                no_load_flag = ''
            else:
                lib_dsuffix = 'so'
                load_flag = '-Wl,-whole-archive'
                no_load_flag = '-Wl,-no-whole-archive'

            os.system(spack_cc + ' -fPIC -shared ' + load_flag +
                      ' libmetis.a ' + no_load_flag + ' -o libmetis.' +
                      lib_dsuffix)
            install('libmetis.' + lib_dsuffix, prefix.lib)

        # Set up and run tests on installation
        symlink(join_path(prefix.share, 'io.c'), 'io.c')
        symlink(join_path(prefix.share, 'mtest.c'), 'mtest.c')
        os.system(spack_cc + ' -I%s' % prefix.include + ' -c io.c')
        os.system(spack_cc + ' -I%s' % prefix.include +
                  ' -L%s' % prefix.lib + ' -lmetis mtest.c io.o -o mtest')
        _4eltgraph = join_path(prefix.share, '4elt.graph')
        test_mgraph = join_path(prefix.share, 'test.mgraph')
        metis_mesh = join_path(prefix.share, 'metis.mesh')
        kmetis = join_path(prefix.bin, 'kmetis')
        os.system('./mtest ' + _4eltgraph)
        os.system(kmetis + ' ' + _4eltgraph + ' 40')
        os.system(join_path(prefix.bin, 'onmetis') + ' ' + _4eltgraph)
        os.system(join_path(prefix.bin, 'pmetis') + ' ' + test_mgraph + ' 2')
        os.system(kmetis + ' ' + test_mgraph + ' 2')
        os.system(kmetis + ' ' + test_mgraph + ' 5')
        os.system(join_path(prefix.bin, 'partnmesh') + metis_mesh + ' 10')
        os.system(join_path(prefix.bin, 'partdmesh') + metis_mesh + ' 10')
        os.system(join_path(prefix.bin, 'mesh2dual') + metis_mesh)


    @when('@5:')
    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        options.append('-DGKLIB_PATH:PATH={metis_source}/GKlib'.format(metis_source=source_directory))
        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')

        if '+debug' in spec:
            options.extend(['-DDEBUG:BOOL=ON',
                            '-DCMAKE_BUILD_TYPE:STRING=Debug'])

        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        metis_header = join_path(source_directory, 'include', 'metis.h')

        if '+idx64' in spec:
            filter_file('IDXTYPEWIDTH 32', 'IDXTYPEWIDTH 64', metis_header)

        if '+double' in spec:
            filter_file('REALTYPEWIDTH 32', 'REALTYPEWIDTH 64', metis_header)

        # Make clang 7.3 happy.
        # Prevents "ld: section __DATA/__thread_bss extends beyond end of file"
        # See upstream LLVM issue https://llvm.org/bugs/show_bug.cgi?id=27059
        # Adopted from https://github.com/Homebrew/homebrew-science/blob/master/metis.rb
        if spec.satisfies('%clang@7.3.0'):
            filter_file('#define MAX_JBUFS 128', '#define MAX_JBUFS 24', join_path(source_directory, 'GKlib', 'error.c'))

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
            # now run some tests:
            for f in ["4elt", "copter2", "mdual"]:
                graph = join_path(source_directory,'graphs','%s.graph' % f)
                Executable(join_path(prefix.bin,'graphchk'))(graph)
                Executable(join_path(prefix.bin,'gpmetis'))(graph,'2')
                Executable(join_path(prefix.bin,'ndmetis'))(graph)

            graph = join_path(source_directory,'graphs','test.mgraph')
            Executable(join_path(prefix.bin,'gpmetis'))(graph,'2')
            graph = join_path(source_directory,'graphs','metis.mesh')
            Executable(join_path(prefix.bin,'mpmetis'))(graph,'2')

            # install GKlib headers, which will be needed for ParMETIS
            GKlib_dist = join_path(prefix.include,'GKlib')
            mkdirp(GKlib_dist)
            fs = glob.glob(join_path(source_directory,'GKlib',"*.h"))
            for f in fs:
                install(f, GKlib_dist)
