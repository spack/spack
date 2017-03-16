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
from spack.util.environment import *
import shutil


class R(AutotoolsPackage):
    """R is 'GNU S', a freely available language and environment for
    statistical computing and graphics which provides a wide variety of
    statistical and graphical techniques: linear and nonlinear modelling,
    statistical tests, time series analysis, classification, clustering, etc.
    Please consult the R project homepage for further information."""

    homepage = "https://www.r-project.org"
    url = "https://cloud.r-project.org/src/base/R-3/R-3.3.2.tar.gz"

    extendable = True

    version('3.3.2', '2437014ef40641cdc9673e89c040b7a8')
    version('3.3.1', 'f50a659738b73036e2f5635adbd229c5')
    version('3.3.0', '5a7506c8813432d1621c9725e86baf7a')
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

    # Virtual dependencies
    depends_on('blas', when='+external-lapack')
    depends_on('lapack', when='+external-lapack')

    # Concrete dependencies
    depends_on('readline')
    depends_on('ncurses')
    depends_on('icu4c')
    depends_on('glib')
    depends_on('zlib@1.2.5:')
    depends_on('bzip2')
    depends_on('libtiff')
    depends_on('jpeg')
    depends_on('cairo')
    depends_on('cairo+X', when='+X')
    depends_on('cairo~X', when='~X')
    depends_on('pango')
    depends_on('freetype')
    depends_on('tcl')
    depends_on('tk')
    depends_on('tk+X', when='+X')
    depends_on('tk~X', when='~X')
    depends_on('libx11', when='+X')
    depends_on('libxt', when='+X')
    depends_on('curl')
    depends_on('pcre')
    depends_on('jdk')

    patch('zlib.patch', when='@:3.3.2')

    @property
    def etcdir(self):
        return join_path(prefix, 'rlib', 'R', 'etc')

    def configure_args(self):
        spec   = self.spec
        prefix = self.prefix

        config_args = [
            '--libdir={0}'.format(join_path(prefix, 'rlib')),
            '--enable-R-shlib',
            '--enable-BLAS-shlib',
            '--enable-R-framework=no'
        ]

        if '+external-lapack' in spec:
            config_args.extend([
                '--with-blas',
                '--with-lapack'
            ])

        if '+X' in spec:
            config_args.append('--with-x')
        else:
            config_args.append('--without-x')

        return config_args

    @run_after('install')
    def copy_makeconf(self):
        # Make a copy of Makeconf because it will be needed to properly build R
        # dependencies in Spack.
        src_makeconf = join_path(self.etcdir, 'Makeconf')
        dst_makeconf = join_path(self.etcdir, 'Makeconf.spack')
        shutil.copy(src_makeconf, dst_makeconf)

    @run_after('install')
    def filter_compilers(self):
        """Run after install to tell the configuration files and Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC and CXX set to Spack's generic
        cc and c++. We want them to be bound to whatever compiler
        they were built with."""

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        filter_file(env['CC'], self.compiler.cc,
                    join_path(self.etcdir, 'Makeconf'), **kwargs)
        filter_file(env['CXX'], self.compiler.cxx,
                    join_path(self.etcdir, 'Makeconf'), **kwargs)
        filter_file(env['F77'], self.compiler.f77,
                    join_path(self.etcdir, 'Makeconf'), **kwargs)
        filter_file(env['FC'], self.compiler.fc,
                    join_path(self.etcdir, 'Makeconf'), **kwargs)

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
