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
import glob
import sys
import os


class Metis(Package):
    """METIS is a set of serial programs for partitioning graphs, partitioning
       finite element meshes, and producing fill reducing orderings for sparse
       matrices. The algorithms implemented in METIS are based on the
       multilevel recursive-bisection, multilevel k-way, and multi-constraint
       partitioning schemes."""

    homepage = "http://glaros.dtc.umn.edu/gkhome/metis/metis/overview"
    base_url = "http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis"

    version('5.1.0', '5465e67079419a69e0116de24fce58fe')
    version('5.0.2', 'acb521a4e8c2e6dd559a7f9abd0468c5')
    version('4.0.3', 'd3848b454532ef18dc83e4fb160d1e10')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds the library in debug mode')
    variant('gdb', default=False, description='Enables gdb support')

    variant('idx64', default=False, description='Use int64_t as default index type')
    variant('real64', default=False, description='Use double precision floating point types')

    depends_on('cmake@2.8:', when='@5:')  # build-time dependency

    patch('install_gklib_defs_rename.patch', when='@5:')

    def url_for_version(self, version):
        verdir = 'OLD/' if version < Version('4.0.3') else ''
        return '%s/%smetis-%s.tar.gz' % (Metis.base_url, verdir, version)

    @when('@:4')
    def install(self, spec, prefix):
        # Process library spec and options
        unsupp_vars = [v for v in ('+gdb', '+idx64', '+real64') if v in spec]
        if unsupp_vars:
            msg = 'Given variants %s are unsupported by METIS 4!' % unsupp_vars
            raise InstallError(msg)

        options = ['COPTIONS=-fPIC']
        if '+debug' in spec:
            options.append('OPTFLAGS=-g -O0')
        make(*options)

        # Compile and install library files
        ccompile = Executable(self.compiler.cc)

        mkdir(prefix.bin)
        binfiles = ('pmetis', 'kmetis', 'oemetis', 'onmetis', 'partnmesh',
                    'partdmesh', 'mesh2nodal', 'mesh2dual', 'graphchk')
        for binfile in binfiles:
            install(binfile, prefix.bin)

        mkdir(prefix.lib)
        install('libmetis.a', prefix.lib)

        mkdir(prefix.include)
        for h in glob.glob(join_path('Lib', '*.h')):
            install(h, prefix.include)

        mkdir(prefix.share)
        sharefiles = (('Graphs', '4elt.graph'), ('Graphs', 'metis.mesh'),
                      ('Graphs', 'test.mgraph'))
        for sharefile in tuple(join_path(*sf) for sf in sharefiles):
            install(sharefile, prefix.share)

        if '+shared' in spec:
            if sys.platform == 'darwin':
                lib_dsuffix = 'dylib'
                load_flag = '-Wl,-all_load'
                no_load_flag = ''
            else:
                lib_dsuffix = 'so'
                load_flag = '-Wl,-whole-archive'
                no_load_flag = '-Wl,-no-whole-archive'

            ccompile('-fPIC', '-shared', load_flag, 'libmetis.a', no_load_flag,
                     '-o', '%s/libmetis.%s' % (prefix.lib, lib_dsuffix))

        # Set up and run tests on installation
        ccompile('-I%s' % prefix.include, '-L%s' % prefix.lib,
                 '-Wl,-rpath=%s' % (prefix.lib if '+shared' in spec else ''),
                 join_path('Programs', 'io.o'), join_path('Test', 'mtest.c'),
                 '-o', '%s/mtest' % prefix.bin, '-lmetis', '-lm')

        test_bin = lambda testname: join_path(prefix.bin, testname)
        test_graph = lambda graphname: join_path(prefix.share, graphname)

        graph = test_graph('4elt.graph')
        os.system('%s %s' % (test_bin('mtest'), graph))
        os.system('%s %s 40' % (test_bin('kmetis'), graph))
        os.system('%s %s' % (test_bin('onmetis'), graph))
        graph = test_graph('test.mgraph')
        os.system('%s %s 2' % (test_bin('pmetis'), graph))
        os.system('%s %s 2' % (test_bin('kmetis'), graph))
        os.system('%s %s 5' % (test_bin('kmetis'), graph))
        graph = test_graph('metis.mesh')
        os.system('%s %s 10' % (test_bin('partnmesh'), graph))
        os.system('%s %s 10' % (test_bin('partdmesh'), graph))
        os.system('%s %s' % (test_bin('mesh2dual'), graph))

    @when('@5:')
    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        options.append('-DGKLIB_PATH:PATH=%s/GKlib' % source_directory)
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
        if '+real64' in spec:
            filter_file('REALTYPEWIDTH 32', 'REALTYPEWIDTH 64', metis_header)

        # Make clang 7.3 happy.
        # Prevents "ld: section __DATA/__thread_bss extends beyond end of file"
        # See upstream LLVM issue https://llvm.org/bugs/show_bug.cgi?id=27059
        # and https://github.com/Homebrew/homebrew-science/blob/master/metis.rb
        if spec.satisfies('%clang@7.3.0'):
            filter_file('#define MAX_JBUFS 128', '#define MAX_JBUFS 24',
                        join_path(source_directory, 'GKlib', 'error.c'))

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make('install')

            # now run some tests:
            for f in ['4elt', 'copter2', 'mdual']:
                graph = join_path(source_directory, 'graphs', '%s.graph' % f)
                Executable(join_path(prefix.bin, 'graphchk'))(graph)
                Executable(join_path(prefix.bin, 'gpmetis'))(graph, '2')
                Executable(join_path(prefix.bin, 'ndmetis'))(graph)

            graph = join_path(source_directory, 'graphs', 'test.mgraph')
            Executable(join_path(prefix.bin, 'gpmetis'))(graph, '2')
            graph = join_path(source_directory, 'graphs', 'metis.mesh')
            Executable(join_path(prefix.bin, 'mpmetis'))(graph, '2')

            # install GKlib headers, which will be needed for ParMETIS
            GKlib_dist = join_path(prefix.include, 'GKlib')
            mkdirp(GKlib_dist)
            hfiles = glob.glob(join_path(source_directory, 'GKlib', '*.h'))
            for hfile in hfiles:
                install(hfile, GKlib_dist)
