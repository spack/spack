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
import functools
import glob
import inspect
import os
import re
from contextlib import closing

import spack
from llnl.util.lang import match_predicate
from spack import *
from spack.util.environment import *


class R(Package):
    """
    R is 'GNU S', a freely available language and environment for statistical computing and graphics which provides a
    wide variety of statistical and graphical techniques: linear and nonlinear modelling, statistical tests, time series
    analysis, classification, clustering, etc. Please consult the R project homepage for further information.
    """
    homepage = "https://www.r-project.org"
    url = "http://cran.cnr.berkeley.edu/src/base/R-3/R-3.1.2.tar.gz"
    
    extendable = True

    version('3.2.3', '1ba3dac113efab69e706902810cc2970')
    version('3.2.2', '57cef5c2e210a5454da1979562a10e5b')
    version('3.2.1', 'c2aac8b40f84e08e7f8c9068de9239a3')
    version('3.2.0', '66fa17ad457d7e618191aa0f52fc402e')
    version('3.1.3', '53a85b884925aa6b5811dfc361d73fc4')
    version('3.1.2', '3af29ec06704cbd08d4ba8d69250ae74')

    variant('external-lapack', default=False, description='Links to externally installed BLAS/LAPACK')

    # Virtual dependencies
    depends_on('blas', when='+external-lapack')
    depends_on('lapack', when='+external-lapack')

    # Concrete dependencies
    depends_on('readline')
    depends_on('ncurses')
    depends_on('icu')
    depends_on('glib')
    depends_on('zlib')
    depends_on('libtiff')
    depends_on('jpeg')
    depends_on('cairo')
    depends_on('pango')
    depends_on('freetype')
    depends_on('tcl')
    depends_on('tk')

    def install(self, spec, prefix):
        rlibdir = join_path(prefix, 'rlib')
        options = ['--prefix=%s' % prefix,
                   '--libdir=%s' % rlibdir,
                   '--enable-R-shlib',
                   '--enable-BLAS-shlib',
                   '--enable-R-framework=no']
        if '+external-lapack' in spec:
            options.extend(['--with-blas', '--with-lapack'])

        configure(*options)
        make()
        make('install')

    # ========================================================================
    # Set up environment to make install easy for R extensions.
    # ========================================================================

    @property
    def r_lib_dir(self):
        return os.path.join('rlib', 'R', 'library')

    def setup_dependent_environment(self, spack_env, run_env, extension_spec):
        # Set R_LIBS to include the library dir for the
        # extension and any other R extensions it depends on.
        r_libs_path = []
        for d in extension_spec.traverse():
            if d.package.extends(self.spec):
                r_libs_path.append(os.path.join(d.prefix, self.r_lib_dir))

        r_libs_path = ':'.join(r_libs_path)
        spack_env.set('R_LIBS', r_libs_path)

        # For run time environment set only the path for extension_spec and prepend it to R_LIBS
        if extension_spec.package.extends(self.spec):
            run_env.prepend_path('R_LIBS', os.path.join(extension_spec.prefix, self.r_lib_dir))


    def setup_dependent_package(self, module, ext_spec):
        """
        Called before R modules' install() methods.

        In most cases, extensions will only need to have one line::

	R('CMD', 'INSTALL', '--library=%s' % self.module.r_lib_dir, '%s' % self.stage.archive_file)
        """
        # R extension builds can have a global R executable function
        module.R = Executable(join_path(self.spec.prefix.bin, 'R'))

        # Add variable for library directry
        module.r_lib_dir = os.path.join(ext_spec.prefix, self.r_lib_dir)

        # Make the site packages directory for extensions, if it does not exist already.
        if ext_spec.package.is_extension:
            mkdirp(module.r_lib_dir)
