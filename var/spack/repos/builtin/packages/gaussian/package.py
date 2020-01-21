# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Gaussian(Package):
    """Gaussian  is a computer program for computational chemistry"""

    homepage = "http://www.gaussian.com/"
    url = "file://{0}/g09.tgz".format(os.getcwd())
    manual_download = True

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

    def setup_run_environment(self, env):
        env.set('g09root', self.prefix)
        env.set('GAUSSIANHOME', self.prefix)
        env.set('GAUSS_EXEDIR', self.prefix.bin)
        env.set('G09_BASIS', self.prefix.bin.basis)
        env.set('GAUSS_LEXEDIR', join_path(self.prefix.bin, 'linda-exe'))
        env.set('GAUSS_ARCHDIR', self.prefix.bin.arch)
        env.set('GAUSS_BSDDIR', self.prefix.bin.bsd)
        env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix.bin,
                         'linda8.2', 'opteron-linux', 'lib'))
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.bin)
