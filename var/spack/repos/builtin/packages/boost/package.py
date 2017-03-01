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
import sys
import os
from glob import glob


class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
       libraries, emphasizing libraries that work well with the C++
       Standard Library.

       Boost libraries are intended to be widely useful, and usable
       across a broad spectrum of applications. The Boost license
       encourages both commercial and non-commercial use.
    """
    homepage = "http://www.boost.org"
    url      = "http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2"
    list_url = "http://sourceforge.net/projects/boost/files/boost/"
    list_depth = 2

    version('1.63.0', '1c837ecd990bb022d07e7aab32b09847')
    version('1.62.0', '5fb94629535c19e48703bdb2b2e9490f')
    version('1.61.0', '6095876341956f65f9d35939ccea1a9f')
    version('1.60.0', '65a840e1a0b13a558ff19eeb2c4f0cbe')
    version('1.59.0', '6aa9a5c6a4ca1016edd0ed1178e3cb87')
    version('1.58.0', 'b8839650e61e9c1c0a89f371dd475546')
    version('1.57.0', '1be49befbdd9a5ce9def2983ba3e7b76')
    version('1.56.0', 'a744cf167b05d72335f27c88115f211d')
    version('1.55.0', 'd6eef4b4cacb2183f2bf265a5a03a354')
    version('1.54.0', '15cb8c0803064faef0c4ddf5bc5ca279')
    version('1.53.0', 'a00d22605d5dbcfb4c9936a9b35bc4c2')
    version('1.52.0', '3a855e0f919107e0ca4de4d84ad3f750')
    version('1.51.0', '4b6bd483b692fd138aef84ed2c8eb679')
    version('1.50.0', '52dd00be775e689f55a987baebccc462')
    version('1.49.0', '0d202cb811f934282dea64856a175698')
    version('1.48.0', 'd1e9a7a7f532bb031a3c175d86688d95')
    version('1.47.0', 'a2dc343f7bc7f83f8941e47ed4a18200')
    version('1.46.1', '7375679575f4c8db605d426fc721d506')
    version('1.46.0', '37b12f1702319b73876b0097982087e0')
    version('1.45.0', 'd405c606354789d0426bc07bea617e58')
    version('1.44.0', 'f02578f5218f217a9f20e9c30e119c6a')
    version('1.43.0', 'dd49767bfb726b0c774f7db0cef91ed1')
    version('1.42.0', '7bf3b4eb841b62ffb0ade2b82218ebe6')
    version('1.41.0', '8bb65e133907db727a2a825c5400d0a6')
    version('1.40.0', 'ec3875caeac8c52c7c129802a8483bd7')
    version('1.39.0', 'a17281fd88c48e0d866e1a12deecbcc0')
    version('1.38.0', '5eca2116d39d61382b8f8235915cb267')
    version('1.37.0', '8d9f990bfb7e83769fa5f1d6f065bc92')
    version('1.36.0', '328bfec66c312150e4c2a78dcecb504b')
    version('1.35.0', 'dce952a7214e72d6597516bcac84048b')
    version('1.34.1', '2d938467e8a448a2c9763e0a9f8ca7e5')
    version('1.34.0', 'ed5b9291ffad776f8757a916e1726ad0')

    default_install_libs = set(['atomic',
                                'chrono',
                                'date_time',
                                'filesystem',
                                'graph',
                                'iostreams',
                                'locale',
                                'log',
                                'math',
                                'program_options',
                                'random',
                                'regex',
                                'serialization',
                                'signals',
                                'system',
                                'test',
                                'thread',
                                'timer',
                                'wave'])

    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    default_noinstall_libs = set(['mpi', 'python'])

    all_libs = default_install_libs | default_noinstall_libs

    for lib in all_libs:
        variant(lib, default=(lib not in default_noinstall_libs),
                description="Compile with {0} library".format(lib))

    variant('debug', default=False,
            description='Switch to the debug version of Boost')
    variant('shared', default=True,
            description="Additionally build shared libraries")
    variant('multithreaded', default=True,
            description="Build multi-threaded versions of libraries")
    variant('singlethreaded', default=False,
            description="Build single-threaded versions of libraries")
    variant('icu', default=False,
            description="Build with Unicode and ICU suport")
    variant('graph', default=False,
            description="Build the Boost Graph library")
    variant('taggedlayout', default=False,
            description="Augment library names with build options")

    depends_on('icu4c', when='+icu')
    depends_on('python', when='+python')
    depends_on('mpi', when='+mpi')
    depends_on('bzip2', when='+iostreams')
    depends_on('zlib', when='+iostreams')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11856
    patch('boost_11856.patch', when='@1.60.0%gcc@4.4.7')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120
    patch('python_jam.patch', when='^python@3:')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125
    patch('boost_10125.patch', when='@1.55.0%gcc@5.0:5.9')

    # Patch fix for IBM XL compiler
    patch('xl_1_62_0_le.patch', when='@1.62.0%xl_r')
    patch('xl_1_62_0_le.patch', when='@1.62.0%xl')

    def url_for_version(self, version):
        """
        Handle Boost's weird URLs,
        which write the version two different ways.
        """
        parts = [str(p) for p in Version(version)]
        dots = ".".join(parts)
        underscores = "_".join(parts)
        return "http://downloads.sourceforge.net/project/boost/boost/%s/boost_%s.tar.bz2" % (dots, underscores)

    def determine_toolset(self, spec):
        if spec.satisfies("platform=darwin"):
            return 'darwin'

        toolsets = {'g++': 'gcc',
                    'icpc': 'intel',
                    'clang++': 'clang',
                    'xlc++': 'xlcpp',
                    'xlc++_r': 'xlcpp'}

        if spec.satisfies('@1.47:'):
            toolsets['icpc'] += '-linux'
        for cc, toolset in toolsets.iteritems():
            if cc in self.compiler.cxx_names:
                return toolset

        # fallback to gcc if no toolset found
        return 'gcc'

    def bjam_python_line(self, spec):
        from os.path import dirname, splitext
        pydir = 'python%s.%s*' % spec['python'].version.version[:2]
        incs = join_path(spec['python'].prefix.include, pydir, "pyconfig.h")
        incs = glob(incs)
        incs = " ".join([dirname(u) for u in incs])

        pylib = 'libpython%s.%s*' % spec['python'].version.version[:2]
        all_libs = join_path(spec['python'].prefix.lib, pylib)
        libs = [u for u in all_libs if splitext(u)[1] == dso_suffix]
        if len(libs) == 0:
            libs = [u for u in all_libs if splitext(u)[1] == '.a']

        libs = " ".join(libs)
        return 'using python : %s : %s : %s : %s ;\n' % (
            spec['python'].version.up_to(2),
            join_path(spec['python'].prefix.bin, 'python'),
            incs, libs
        )

    def determine_bootstrap_options(self, spec, withLibs, options):
        boostToolsetId = self.determine_toolset(spec)
        options.append('--with-toolset=%s' % boostToolsetId)
        options.append("--with-libraries=%s" % ','.join(withLibs))

        if '+python' in spec:
            options.append('--with-python=%s' % python_exe)

        with open('user-config.jam', 'w') as f:
            # Boost may end up using gcc even though clang+gfortran is set in
            # compilers.yaml. Make sure this does not happen:
            if not spec.satisfies('%intel'):
                # using intel-linux : : spack_cxx in user-config.jam leads to
                # error: at project-config.jam:12
                # error: duplicate initialization of intel-linux with the following parameters:  # noqa
                # error: version = <unspecified>
                # error: previous initialization at ./user-config.jam:1
                f.write("using {0} : : {1} ;\n".format(boostToolsetId,
                                                       spack_cxx))

            if '+mpi' in spec:
                f.write('using mpi : %s ;\n' %
                        join_path(spec['mpi'].prefix.bin, 'mpicxx'))
            if '+python' in spec:
                f.write(self.bjam_python_line(spec))

    def determine_b2_options(self, spec, options):
        if '+debug' in spec:
            options.append('variant=debug')
        else:
            options.append('variant=release')

        if '+icu_support' in spec:
            options.extend(['-s', 'ICU_PATH=%s' % spec['icu'].prefix])

        if '+iostreams' in spec:
            options.extend([
                '-s', 'BZIP2_INCLUDE=%s' % spec['bzip2'].prefix.include,
                '-s', 'BZIP2_LIBPATH=%s' % spec['bzip2'].prefix.lib,
                '-s', 'ZLIB_INCLUDE=%s' % spec['zlib'].prefix.include,
                '-s', 'ZLIB_LIBPATH=%s' % spec['zlib'].prefix.lib])

        linkTypes = ['static']
        if '+shared' in spec:
            linkTypes.append('shared')

        threadingOpts = []
        if '+multithreaded' in spec:
            threadingOpts.append('multi')
        if '+singlethreaded' in spec:
            threadingOpts.append('single')
        if not threadingOpts:
            raise RuntimeError("At least one of {singlethreaded, " +
                               "multithreaded} must be enabled")

        if '+taggedlayout' in spec:
            layout = 'tagged'
        else:
            if len(threadingOpts) > 1:
                raise RuntimeError("Cannot build both single and " +
                                   "multi-threaded targets with system layout")
            layout = 'system'

        options.extend([
            'link=%s' % ','.join(linkTypes),
            '--layout=%s' % layout
        ])

        if not spec.satisfies('%intel'):
            options.extend([
                'toolset=%s' % self.determine_toolset(spec)
            ])

        # clang is not officially supported for pre-compiled headers
        # and at least in clang 3.9 still fails to build
        #   http://www.boost.org/build/doc/html/bbv2/reference/precompiled_headers.html
        #   https://svn.boost.org/trac/boost/ticket/12496
        if spec.satisfies('%clang'):
            options.extend(['pch=off'])

        return threadingOpts

    def add_buildopt_symlinks(self, prefix):
        with working_dir(prefix.lib):
            for lib in os.listdir(os.curdir):
                prefix, remainder = lib.split('.', 1)
                symlink(lib, '%s-mt.%s' % (prefix, remainder))

    def install(self, spec, prefix):
        # On Darwin, Boost expects the Darwin libtool. However, one of the
        # dependencies may have pulled in Spack's GNU libtool, and these two
        # are not compatible. We thus create a symlink to Darwin's libtool
        # and add it at the beginning of PATH.
        if sys.platform == 'darwin':
            newdir = os.path.abspath('darwin-libtool')
            mkdirp(newdir)
            force_symlink('/usr/bin/libtool', join_path(newdir, 'libtool'))
            env['PATH'] = newdir + ':' + env['PATH']

        withLibs = list()
        for lib in Boost.all_libs:
            if "+{0}".format(lib) in spec:
                withLibs.append(lib)
        if not withLibs:
            # if no libraries are specified for compilation, then you dont have
            # to configure/build anything, just copy over to the prefix
            # directory.
            src = join_path(self.stage.source_path, 'boost')
            mkdirp(join_path(prefix, 'include'))
            dst = join_path(prefix, 'include', 'boost')
            install_tree(src, dst)
            return

        # Remove libraries that the release version does not support
        if not spec.satisfies('@1.54.0:'):
            withLibs.remove('log')
        if not spec.satisfies('@1.53.0:'):
            withLibs.remove('atomic')
        if not spec.satisfies('@1.48.0:'):
            withLibs.remove('locale')
        if not spec.satisfies('@1.47.0:'):
            withLibs.remove('chrono')
        if not spec.satisfies('@1.43.0:'):
            withLibs.remove('random')
        if '+graph' in spec and '+mpi' in spec:
            withLibs.remove('graph')
            withLibs.append('graph_parallel')

        # to make Boost find the user-config.jam
        env['BOOST_BUILD_PATH'] = './'

        bootstrap = Executable('./bootstrap.sh')

        bootstrap_options = ['--prefix=%s' % prefix]
        self.determine_bootstrap_options(spec, withLibs, bootstrap_options)

        bootstrap(*bootstrap_options)

        # b2 used to be called bjam, before 1.47 (sigh)
        b2name = './b2' if spec.satisfies('@1.47:') else './bjam'

        b2 = Executable(b2name)
        b2_options = ['-j', '%s' % make_jobs]

        threadingOpts = self.determine_b2_options(spec, b2_options)

        b2('--clean')

        # In theory it could be done on one call but it fails on
        # Boost.MPI if the threading options are not separated.
        for threadingOpt in threadingOpts:
            b2('install', 'threading=%s' % threadingOpt, *b2_options)

        if '+multithreaded' in spec and '~taggedlayout' in spec:
            self.add_buildopt_symlinks(prefix)

        # The shared libraries are not installed correctly
        # on Darwin; correct this
        if (sys.platform == 'darwin') and ('+shared' in spec):
            fix_darwin_install_name(prefix.lib)
