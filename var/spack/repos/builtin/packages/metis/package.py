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

    variant('shared', default=True, description='Enables the build of shared libraries.')
    variant('debug', default=False, description='Builds the library in debug mode.')
    variant('gdb', default=False, description='Enables gdb support.')

    variant('int64', default=False, description='Sets the bit width of METIS\'s index type to 64.')
    variant('real64', default=False, description='Sets the bit width of METIS\'s real type to 64.')

    depends_on('cmake@2.8:', when='@5:', type='build')

    patch('install_gklib_defs_rename.patch', when='@5:')

    def url_for_version(self, version):
        verdir = 'OLD/' if version < Version('4.0.3') else ''
        return '%s/%smetis-%s.tar.gz' % (Metis.base_url, verdir, version)

    @when('@:4')
    def patch(self):
        pass

    @when('@5:')
    def patch(self):
        source_path = self.stage.source_path
        metis_header = FileFilter(join_path(source_path, 'include', 'metis.h'))

        metis_header.filter(
            r'(\b)(IDXTYPEWIDTH )(\d+)(\b)',
            r'\1\2{0}\4'.format('64' if '+int64' in self.spec else '32'),
        )
        metis_header.filter(
            r'(\b)(REALTYPEWIDTH )(\d+)(\b)',
            r'\1\2{0}\4'.format('64' if '+real64' in self.spec else '32'),
        )

        # Make clang 7.3 happy.
        # Prevents "ld: section __DATA/__thread_bss extends beyond end of file"
        # See upstream LLVM issue https://llvm.org/bugs/show_bug.cgi?id=27059
        # and https://github.com/Homebrew/homebrew-science/blob/master/metis.rb
        if self.spec.satisfies('%clang@7.3.0'):
            filter_file('#define MAX_JBUFS 128', '#define MAX_JBUFS 24',
                        join_path(source_path, 'GKlib', 'error.c'))

    @when('@:4')
    def install(self, spec, prefix):
        # Process library spec and options
        if any('+{0}'.format(v) in spec for v in ['gdb', 'int64', 'real64']):
            raise InstallError('METIS@:4 does not support the following '
                               'variants: gdb, int64, real64.')

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
            shared_flags = ['-fPIC', '-shared']
            if sys.platform == 'darwin':
                shared_suffix = 'dylib'
                shared_flags.extend(['-Wl,-all_load', 'libmetis.a'])
            else:
                shared_suffix = 'so'
                shared_flags.extend(['-Wl,-whole-archive', 'libmetis.a',
                                     '-Wl,-no-whole-archive'])

            shared_out = '%s/libmetis.%s' % (prefix.lib, shared_suffix)
            shared_flags.extend(['-o', shared_out])

            ccompile(*shared_flags)

        # Set up and run tests on installation
        ccompile('-I%s' % prefix.include, '-L%s' % prefix.lib,
                 '-Wl,-rpath=%s' % (prefix.lib if '+shared' in spec else ''),
                 join_path('Programs', 'io.o'), join_path('Test', 'mtest.c'),
                 '-o', '%s/mtest' % prefix.bin, '-lmetis', '-lm')

        if self.run_tests:
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

            # FIXME: The following code should replace the testing code in the
            # block above since it causes installs to fail when one or more of
            # the Metis tests fail, but it currently doesn't work because the
            # 'mtest', 'onmetis', and 'partnmesh' tests return error codes that
            # trigger false positives for failure.
            """
            Executable(test_bin('mtest'))(test_graph('4elt.graph'))
            Executable(test_bin('kmetis'))(test_graph('4elt.graph'), '40')
            Executable(test_bin('onmetis'))(test_graph('4elt.graph'))

            Executable(test_bin('pmetis'))(test_graph('test.mgraph'), '2')
            Executable(test_bin('kmetis'))(test_graph('test.mgraph'), '2')
            Executable(test_bin('kmetis'))(test_graph('test.mgraph'), '5')

            Executable(test_bin('partnmesh'))(test_graph('metis.mesh'), '10')
            Executable(test_bin('partdmesh'))(test_graph('metis.mesh'), '10')
            Executable(test_bin('mesh2dual'))(test_graph('metis.mesh'))
            """

    @when('@5:')
    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        build_directory = join_path(source_directory, 'build')

        options = std_cmake_args[:]
        options.append('-DGKLIB_PATH:PATH=%s/GKlib' % source_directory)
        options.append('-DCMAKE_INSTALL_NAME_DIR:PATH=%s/lib' % prefix)

        if '+shared' in spec:
            options.append('-DSHARED:BOOL=ON')
        else:
            # Remove all RPATH options 
            # (RPATHxxx options somehow trigger cmake to link dynamically)
            rpath_options = []
            for o in options:
                if o.find('RPATH') >= 0:
                    rpath_options.append(o)
            for o in rpath_options:
                options.remove(o)
        if '+debug' in spec:
            options.extend(['-DDEBUG:BOOL=ON',
                            '-DCMAKE_BUILD_TYPE:STRING=Debug'])
        if '+gdb' in spec:
            options.append('-DGDB:BOOL=ON')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make('install')

            # install GKlib headers, which will be needed for ParMETIS
            GKlib_dist = join_path(prefix.include, 'GKlib')
            mkdirp(GKlib_dist)
            hfiles = glob.glob(join_path(source_directory, 'GKlib', '*.h'))
            for hfile in hfiles:
                install(hfile, GKlib_dist)

        if self.run_tests:
            # FIXME: On some systems, the installed binaries for METIS cannot
            # be executed without first being read.
            ls = which('ls')
            ls('-a', '-l', prefix.bin)

            for f in ['4elt', 'copter2', 'mdual']:
                graph = join_path(source_directory, 'graphs', '%s.graph' % f)
                Executable(join_path(prefix.bin, 'graphchk'))(graph)
                Executable(join_path(prefix.bin, 'gpmetis'))(graph, '2')
                Executable(join_path(prefix.bin, 'ndmetis'))(graph)

            graph = join_path(source_directory, 'graphs', 'test.mgraph')
            Executable(join_path(prefix.bin, 'gpmetis'))(graph, '2')
            graph = join_path(source_directory, 'graphs', 'metis.mesh')
            Executable(join_path(prefix.bin, 'mpmetis'))(graph, '2')
