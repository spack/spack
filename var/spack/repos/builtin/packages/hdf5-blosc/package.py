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

import os
import shutil
import sys

from spack import *

class Hdf5Blosc(Package):
    """Blosc filter for HDF5"""
    homepage = "https://github.com/Blosc/hdf5-blosc"
    url      = "https://github.com/Blosc/hdf5-blosc/archive/master.zip"

    version('master', '02c04acbf4bec66ec8a35bf157d1c9de')

    depends_on("c-blosc")
    depends_on("hdf5")
    depends_on("libtool")

    parallel = False

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
        if sys.platform == 'darwin':
            fix_darwin_install_name(prefix.lib)

        # Build and install plugin manually
        # The plugin requires at least HDF5 1.8.11:
        if spec['hdf5'].satisfies('@1.8.11:'):
            # The plugin does not yet work with Windows:
            if sys.platform not in ('win32', 'cygwin'):
                # cc = which('cc')
                libtool = Executable(join_path(spec['libtool'].prefix.bin,
                                               'libtool'))
                with working_dir('src'):
                    libtool('--mode=compile', '--tag=CC',
                            'cc', '-g', '-O', '-c', 'blosc_plugin.c')
                    libtool('--mode=link', '--tag=CC',
                            'cc', '-g', '-O',
                            '-rpath', prefix.lib,
                            '-o', 'libblosc_plugin.la', 'blosc_plugin.lo')
                    shlibext = 'so' if sys.platform!='darwin' else 'dylib'
                    shlib0 = 'libblosc_plugin.0.%s' % shlibext
                    shutil.copyfile(join_path('.libs', shlib0),
                                    join_path(prefix.lib, shlib0))
                    shlib = 'libblosc_plugin.%s' % shlibext
                    os.symlink(shlib0, join_path(prefix.lib, shlib))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.append_path('HDF5_PLUGIN_PATH', self.spec.prefix.lib)
        run_env.append_path('HDF5_PLUGIN_PATH', self.spec.prefix.lib)
