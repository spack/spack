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
import os


class Gaussian(Package):
    """Gaussian  is a computer program for computational chemistry"""

    homepage = "http://www.gaussian.com/"
    url = "file://{0}/g09.tgz".format(os.getcwd())

    version('09', '7d4c95b535e68e48af183920df427e4e')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
        patch_install_files = ['flc',
                               'linda8.2/opteron-linux/bin/flc',
                               'linda8.2/opteron-linux/bin/LindaLauncher',
                               'linda8.2/opteron-linux/bin/ntsnet',
                               'linda8.2/opteron-linux/bin/pmbuild',
                               'linda8.2/opteron-linux/bin/vntsnet',
                               'ntsnet'
                               ]
        for filename in patch_install_files:
            if os.path.isfile(filename):
                filter_file('/mf/frisch/g09', prefix.bin, join_path(prefix.bin,
                            filename), string='True')
        patch_install_files = ['linda8.2/opteron-linux/bin/ntsnet',
                               'linda8.2/opteron-linux/bin/vntsnet',
                               ]
        for filename in patch_install_files:
            if os.path.isfile(filename):
                filter_file('/usr/bin/linda', prefix.bin, join_path(prefix.bin,
                            filename), string='True')

    def setup_environment(self, spack_env, run_env):
        run_env.set('g09root', self.prefix)
        run_env.set('GAUSSIANHOME', self.prefix)
        run_env.set('GAUSS_EXEDIR', self.prefix.bin)
        run_env.set('G09_BASIS', join_path(self.prefix.bin, 'basis'))
        run_env.set('GAUSS_LEXEDIR', join_path(self.prefix.bin,
                    'linda-exe'))
        run_env.set('GAUSS_ARCHDIR', join_path(self.prefix.bin, 'arch'))
        run_env.set('GAUSS_BSDDIR', join_path(self.prefix.bin, 'bsd'))
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix.bin,
                             'linda8.2/opteron-linux/lib'))
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix.bin)
