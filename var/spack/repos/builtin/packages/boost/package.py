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
import sys
import os


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
    git      = "https://github.com/boostorg/boost.git"
    list_url = "http://sourceforge.net/projects/boost/files/boost/"
    list_depth = 1

    version('develop', branch='develop', submodules=True)
    version('1.68.0', '18863a7cae4d58ae85eb63d400f774f60a383411')
    version('1.67.0', '694ae3f4f899d1a80eb7a3b31b33be73c423c1ae')
    version('1.66.0', 'b6b284acde2ad7ed49b44e856955d7b1ea4e9459')
    version('1.65.1', '41d7542ce40e171f3f7982aff008ff0d')
    version('1.65.0', '5512d3809801b0a1b9dd58447b70915d')
    # NOTE: 1.64.0 seems fine for *most* applications, but if you need
    #       +python and +mpi, there seem to be errors with out-of-date
    #       API calls from mpi/python.
    #       See: https://github.com/spack/spack/issues/3963
    version('1.64.0', '93eecce2abed9d2442c9676914709349')
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
                                'exception',
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

    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
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
    variant('taggedlayout', default=False,
            description="Augment library names with build options")
    variant('versionedlayout', default=False,
            description="Augment library layout with versioned subdirs")
    variant('clanglibcpp', default=False,
            description='Compile with clang libc++ instead of libstdc++')
    variant('numpy', default=False,
            description='Build the Boost NumPy library (requires +python)')

    depends_on('icu4c', when='+icu')
    depends_on('python', when='+python')
    depends_on('mpi', when='+mpi')
    depends_on('bzip2', when='+iostreams')
    depends_on('zlib', when='+iostreams')
    depends_on('py-numpy', when='+numpy', type=('build', 'run'))

    conflicts('+taggedlayout', when='+versionedlayout')
    conflicts('+numpy', when='~python')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11856
    patch('boost_11856.patch', when='@1.60.0%gcc@4.4.7')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120
    patch('python_jam.patch', when='@1.56.0: ^python@3:')
    patch('python_jam_pre156.patch', when='@:1.55.0 ^python@3:')

    # Patch fix for IBM XL compiler
    patch('xl_1_62_0_le.patch', when='@1.62.0%xl_r')
    patch('xl_1_62_0_le.patch', when='@1.62.0%xl')

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125
    patch('call_once_variadic.patch', when='@1.54.0:1.55.9999%gcc@5.0:5.9')

    # Patch fix for PGI compiler
    patch('boost_1.67.0_pgi.patch', when='@1.67.0%pgi')
    patch('boost_1.63.0_pgi.patch', when='@1.63.0%pgi')
    patch('boost_1.63.0_pgi_17.4_workaround.patch', when='@1.63.0%pgi@17.4')

    def url_for_version(self, version):
        if version >= Version('1.63.0'):
            url = "https://dl.bintray.com/boostorg/release/{0}/source/boost_{1}.tar.bz2"
        else:
            url = "http://downloads.sourceforge.net/project/boost/boost/{0}/boost_{1}.tar.bz2"

        return url.format(version.dotted, version.underscored)

    def determine_toolset(self, spec):
        if spec.satisfies("platform=darwin"):
            return 'darwin'

        toolsets = {'g++': 'gcc',
                    'icpc': 'intel',
                    'clang++': 'clang',
                    'xlc++': 'xlcpp',
                    'xlc++_r': 'xlcpp',
                    'pgc++': 'pgi'}

        if spec.satisfies('@1.47:'):
            toolsets['icpc'] += '-linux'
        for cc, toolset in toolsets.items():
            if cc in self.compiler.cxx_names:
                return toolset

        # fallback to gcc if no toolset found
        return 'gcc'

    def bjam_python_line(self, spec):
        # avoid "ambiguous key" error
        if spec.satisfies('@:1.58'):
            return ''

        return 'using python : {0} : {1} : {2} : {3} ;\n'.format(
            spec['python'].version.up_to(2),
            spec['python'].command.path,
            spec['python'].headers.directories[0],
            spec['python'].libs[0]
        )

    def determine_bootstrap_options(self, spec, with_libs, options):
        boost_toolset_id = self.determine_toolset(spec)
        options.append('--with-toolset=%s' % boost_toolset_id)
        options.append("--with-libraries=%s" % ','.join(with_libs))

        if '+python' in spec:
            options.append('--with-python=%s' % spec['python'].command.path)

        with open('user-config.jam', 'w') as f:
            # Boost may end up using gcc even though clang+gfortran is set in
            # compilers.yaml. Make sure this does not happen:
            if not spec.satisfies('%intel'):
                # using intel-linux : : spack_cxx in user-config.jam leads to
                # error: at project-config.jam:12
                # error: duplicate initialization of intel-linux with the following parameters:  # noqa
                # error: version = <unspecified>
                # error: previous initialization at ./user-config.jam:1
                f.write("using {0} : : {1} ;\n".format(boost_toolset_id,
                                                       spack_cxx))

            if '+mpi' in spec:

                # Use the correct mpi compiler.  If the compiler options are
                # empty or undefined, Boost will attempt to figure out the
                # correct options by running "${mpicxx} -show" or something
                # similar, but that doesn't work with the Cray compiler
                # wrappers.  Since Boost doesn't use the MPI C++ bindings,
                # that can be used as a compiler option instead.

                mpi_line = 'using mpi : %s' % spec['mpi'].mpicxx

                if 'platform=cray' in spec:
                    mpi_line += ' : <define>MPICH_SKIP_MPICXX'

                f.write(mpi_line + ' ;\n')

            if '+python' in spec:
                f.write(self.bjam_python_line(spec))

    def cxxstd_to_flag(self, std):
        flag = ''
        if self.spec.variants['cxxstd'].value == '98':
            flag = self.compiler.cxx98_flag
        elif self.spec.variants['cxxstd'].value == '11':
            flag = self.compiler.cxx11_flag
        elif self.spec.variants['cxxstd'].value == '14':
            flag = self.compiler.cxx14_flag
        elif self.spec.variants['cxxstd'].value == '17':
            flag = self.compiler.cxx17_flag
        elif self.spec.variants['cxxstd'].value == 'default':
            # Let the compiler do what it usually does.
            pass
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die("INTERNAL ERROR: cannot accommodate unexpected variant ",
                    "cxxstd={0}".format(spec.variants['cxxstd'].value))
        return flag

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

        link_types = ['static']
        if '+shared' in spec:
            link_types.append('shared')

        threading_opts = []
        if '+multithreaded' in spec:
            threading_opts.append('multi')
        if '+singlethreaded' in spec:
            threading_opts.append('single')
        if not threading_opts:
            raise RuntimeError("At least one of {singlethreaded, " +
                               "multithreaded} must be enabled")

        if '+taggedlayout' in spec:
            layout = 'tagged'
        elif '+versionedlayout' in spec:
            layout = 'versioned'
        else:
            if len(threading_opts) > 1:
                raise RuntimeError("Cannot build both single and " +
                                   "multi-threaded targets with system layout")
            layout = 'system'

        options.extend([
            'link=%s' % ','.join(link_types),
            '--layout=%s' % layout
        ])

        if not spec.satisfies('%intel'):
            options.extend([
                'toolset=%s' % self.determine_toolset(spec)
            ])

        # Other C++ flags.
        cxxflags = []

        # Deal with C++ standard.
        if spec.satisfies('@1.66:'):
            if spec.variants['cxxstd'].value != 'default':
                options.append('cxxstd={0}'.format(
                    spec.variants['cxxstd'].value))
        else:  # Add to cxxflags for older Boost.
            flag = self.cxxstd_to_flag(spec.variants['cxxstd'].value)
            if flag:
                cxxflags.append(flag)

        # clang is not officially supported for pre-compiled headers
        # and at least in clang 3.9 still fails to build
        #   http://www.boost.org/build/doc/html/bbv2/reference/precompiled_headers.html
        #   https://svn.boost.org/trac/boost/ticket/12496
        if spec.satisfies('%clang'):
            options.extend(['pch=off'])
            if '+clanglibcpp' in spec:
                cxxflags.append('-stdlib=libc++')
                options.extend(['toolset=clang',
                                'linkflags="-stdlib=libc++"'])

        if cxxflags:
            options.append('cxxflags="{0}"'.format(' '.join(cxxflags)))

        return threading_opts

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

        with_libs = list()
        for lib in Boost.all_libs:
            if "+{0}".format(lib) in spec:
                with_libs.append(lib)
        if not with_libs:
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
            with_libs.remove('log')
        if not spec.satisfies('@1.53.0:'):
            with_libs.remove('atomic')
        if not spec.satisfies('@1.48.0:'):
            with_libs.remove('locale')
        if not spec.satisfies('@1.47.0:'):
            with_libs.remove('chrono')
        if not spec.satisfies('@1.43.0:'):
            with_libs.remove('random')
        if not spec.satisfies('@1.39.0:'):
            with_libs.remove('exception')
        if '+graph' in spec and '+mpi' in spec:
            with_libs.append('graph_parallel')

        # to make Boost find the user-config.jam
        env['BOOST_BUILD_PATH'] = self.stage.source_path

        bootstrap = Executable('./bootstrap.sh')

        bootstrap_options = ['--prefix=%s' % prefix]
        self.determine_bootstrap_options(spec, with_libs, bootstrap_options)

        bootstrap(*bootstrap_options)

        # b2 used to be called bjam, before 1.47 (sigh)
        b2name = './b2' if spec.satisfies('@1.47:') else './bjam'

        b2 = Executable(b2name)
        jobs = make_jobs
        # in 1.59 max jobs became dynamic
        if jobs > 64 and spec.satisfies('@:1.58'):
            jobs = 64

        b2_options = [
            '-j', '%s' % jobs,
            '--user-config=%s' % os.path.join(
                self.stage.source_path, 'user-config.jam')
        ]

        threading_opts = self.determine_b2_options(spec, b2_options)

        b2('--clean')

        # In theory it could be done on one call but it fails on
        # Boost.MPI if the threading options are not separated.
        for threadingOpt in threading_opts:
            b2('install', 'threading=%s' % threadingOpt, *b2_options)

        if '+multithreaded' in spec and '~taggedlayout' in spec:
            self.add_buildopt_symlinks(prefix)

        # The shared libraries are not installed correctly
        # on Darwin; correct this
        if (sys.platform == 'darwin') and ('+shared' in spec):
            fix_darwin_install_name(prefix.lib)
