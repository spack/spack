# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack import *


class R(AutotoolsPackage):
    """R is 'GNU S', a freely available language and environment for
    statistical computing and graphics which provides a wide variety of
    statistical and graphical techniques: linear and nonlinear modelling,
    statistical tests, time series analysis, classification, clustering, etc.
    Please consult the R project homepage for further information."""

    homepage = "https://www.r-project.org"
    url = "https://cloud.r-project.org/src/base/R-3/R-3.4.3.tar.gz"

    extendable = True

    version('3.6.1', sha256='5baa9ebd3e71acecdcc3da31d9042fb174d55a42829f8315f2457080978b1389')
    version('3.6.0', sha256='36fcac3e452666158e62459c6fc810adc247c7109ed71c5b6c3ad5fc2bf57509')
    version('3.5.3', sha256='2bfa37b7bd709f003d6b8a172ddfb6d03ddd2d672d6096439523039f7a8e678c')
    version('3.5.2', sha256='e53d8c3cf20f2b8d7a9c1631b6f6a22874506fb392034758b3bb341c586c5b62')
    version('3.5.1', sha256='0463bff5eea0f3d93fa071f79c18d0993878fd4f2e18ae6cf22c1639d11457ed')
    version('3.5.0', 'c0455dbfa76ca807e4dfa93d49dcc817')
    version('3.4.4', '9d6f73be072531e95884c7965ff80cd8')
    version('3.4.3', 'bc55db54f992fda9049201ca62d2a584')
    version('3.4.2', '1cd6d37850188e7f190f1eb94a24ca1f')
    version('3.4.1', '3a79c01dc0527c62e80ffb1c489297ea')
    version('3.4.0', '75083c23d507b9c16d5c6afbd7a827e7')
    version('3.3.3', '0ac211ec15e813a24f8f4a5a634029a4')
    version('3.3.2', '2437014ef40641cdc9673e89c040b7a8')
    version('3.3.1', 'f50a659738b73036e2f5635adbd229c5')
    version('3.3.0', '5a7506c8813432d1621c9725e86baf7a')
    version('3.2.5', '7b23ee70cfb383be3bd4360e3c71d8c3')
    version('3.2.3', '1ba3dac113efab69e706902810cc2970')
    version('3.2.2', '57cef5c2e210a5454da1979562a10e5b')
    version('3.2.1', 'c2aac8b40f84e08e7f8c9068de9239a3')
    version('3.2.0', '66fa17ad457d7e618191aa0f52fc402e')
    version('3.1.3', '53a85b884925aa6b5811dfc361d73fc4')
    version('3.1.2', '3af29ec06704cbd08d4ba8d69250ae74')

    variant('external-lapack', default=False,
            description='Links to externally installed BLAS/LAPACK')
    variant('X', default=False,
            description='Enable X11 support (call configure --with-x)')
    variant('memory_profiling', default=False,
            description='Enable memory profiling')
    variant('rmath', default=False,
            description='Build standalone Rmath library')

    # Virtual dependencies
    depends_on('blas', when='+external-lapack')
    depends_on('lapack', when='+external-lapack')

    # Concrete dependencies.
    depends_on('readline')
    depends_on('ncurses')
    depends_on('icu4c')
    depends_on('glib')
    depends_on('zlib@1.2.5:')
    depends_on('bzip2')
    depends_on('libtiff')
    depends_on('jpeg')
    depends_on('cairo+pdf')
    depends_on('cairo+X', when='+X')
    depends_on('cairo~X', when='~X')
    depends_on('pango')
    depends_on('pango+X', when='+X')
    depends_on('pango~X', when='~X')
    depends_on('freetype')
    depends_on('tcl')
    depends_on('tk', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxt', when='+X')
    depends_on('libxmu', when='+X')
    depends_on('curl')
    depends_on('pcre')
    depends_on('java')

    patch('zlib.patch', when='@:3.3.2')

    filter_compiler_wrappers(
        'Makeconf', relative_root=os.path.join('rlib', 'R', 'etc')
    )

    @property
    def etcdir(self):
        return join_path(prefix, 'rlib', 'R', 'etc')

    @run_after('build')
    def build_rmath(self):
        if '+rmath' in self.spec:
            with working_dir('src/nmath/standalone'):
                make()

    @run_after('install')
    def install_rmath(self):
        if '+rmath' in self.spec:
            with working_dir('src/nmath/standalone'):
                make('install')

    def configure_args(self):
        spec   = self.spec
        prefix = self.prefix

        tcl_config_path = join_path(spec['tcl'].prefix.lib, 'tclConfig.sh')

        config_args = [
            '--libdir={0}'.format(join_path(prefix, 'rlib')),
            '--enable-R-shlib',
            '--enable-BLAS-shlib',
            '--enable-R-framework=no',
            '--with-tcl-config={0}'.format(tcl_config_path),
            'LDFLAGS=-L{0} -Wl,-rpath,{0}'.format(join_path(prefix, 'rlib',
                                                            'R', 'lib')),
        ]
        if '^tk' in spec:
            tk_config_path = join_path(spec['tk'].prefix.lib, 'tkConfig.sh')
            config_args.append('--with-tk-config={0}'.format(tk_config_path))

        if '+external-lapack' in spec:
            if '^mkl' in spec and 'gfortran' in self.compiler.fc:
                mkl_re = re.compile(r'(mkl_)intel(_i?lp64\b)')
                config_args.extend([
                    mkl_re.sub(r'\g<1>gf\g<2>',
                               '--with-blas={0}'.format(
                                   spec['blas'].libs.ld_flags)),
                    '--with-lapack'
                ])
            else:
                config_args.extend([
                    '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
                    '--with-lapack'
                ])

        if '+X' in spec:
            config_args.append('--with-x')
        else:
            config_args.append('--without-x')

        if '+memory_profiling' in spec:
            config_args.append('--enable-memory-profiling')

        # Set FPICFLAGS for compilers except 'gcc'.
        if self.compiler.name != 'gcc':
            config_args.append('FPICFLAGS={0}'.format(self.compiler.pic_flag))

        return config_args

    @run_after('install')
    def copy_makeconf(self):
        # Make a copy of Makeconf because it will be needed to properly build R
        # dependencies in Spack.
        src_makeconf = join_path(self.etcdir, 'Makeconf')
        dst_makeconf = join_path(self.etcdir, 'Makeconf.spack')
        install(src_makeconf, dst_makeconf)

    # ========================================================================
    # Set up environment to make install easy for R extensions.
    # ========================================================================

    @property
    def r_lib_dir(self):
        return join_path('rlib', 'R', 'library')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Set R_LIBS to include the library dir for the
        # extension and any other R extensions it depends on.
        r_libs_path = []
        for d in dependent_spec.traverse(
                deptype=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                r_libs_path.append(join_path(d.prefix, self.r_lib_dir))

        r_libs_path = ':'.join(r_libs_path)
        spack_env.set('R_LIBS', r_libs_path)
        spack_env.set('R_MAKEVARS_SITE',
                      join_path(self.etcdir, 'Makeconf.spack'))

        # Use the number of make_jobs set in spack. The make program will
        # determine how many jobs can actually be started.
        spack_env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

        # For run time environment set only the path for dependent_spec and
        # prepend it to R_LIBS
        if dependent_spec.package.extends(self.spec):
            run_env.prepend_path('R_LIBS', join_path(
                dependent_spec.prefix, self.r_lib_dir))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'rlib', 'R', 'lib'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'rlib', 'R', 'lib'))
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'rlib', 'R', 'include'))

    def setup_dependent_package(self, module, dependent_spec):
        """Called before R modules' install() methods. In most cases,
        extensions will only need to have one line:
            R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
              self.stage.source_path)"""

        # R extension builds can have a global R executable function
        module.R = Executable(join_path(self.spec.prefix.bin, 'R'))

        # Add variable for library directry
        module.r_lib_dir = join_path(dependent_spec.prefix, self.r_lib_dir)

        # Make the site packages directory for extensions, if it does not exist
        # already.
        if dependent_spec.package.is_extension:
            mkdirp(module.r_lib_dir)
