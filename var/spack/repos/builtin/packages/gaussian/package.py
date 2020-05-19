# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os


class Gaussian(Package):
    """Gaussian  is a computer program for computational chemistry"""

    homepage = "http://www.gaussian.com/"
    manual_download = True

    linda_files_to_patch = {
        "09-D.01": ['flc',
                    'linda8.2/opteron-linux/bin/LindaLauncher',
                    'linda8.2/opteron-linux/bin/flc',
                    'linda8.2/opteron-linux/bin/ntsnet',
                    'linda8.2/opteron-linux/bin/pmbuild',
                    'linda8.2/opteron-linux/bin/vntsnet',
                    'ntsnet'],
        "16-B.01": ['clc',
                    'flc',
                    'linda9.1/linux64bit/bin/LindaLauncher',
                    'linda9.1/linux64bit/bin/c++lc',
                    'linda9.1/linux64bit/bin/clc',
                    'linda9.1/linux64bit/bin/flc',
                    'linda9.1/linux64bit/bin/ntsnet',
                    'linda9.1/linux64bit/bin/pmbuild',
                    'linda9.1/linux64bit/bin/vntsnet',
                    'ntsnet'],
    }

    linda_path_to_filter = {
        "09-D.01": "/mf/fernando/Gaussian/g09_D.01-build/g09",
        "16-B.01": "/mf/fernando/Gaussian/g16_B.01_AVX2/g16"
    }

    linda_directory = {
        "09-D.01": "linda8.2",
        "16-B.01": "linda9.1"
    }

    version('16-B.01', sha256='0b2cf60aa85d2c8c8e7547446e60e8e8cb67eec20e5f13c4a3e4e7616dcdf122')
    version('09-D.01', sha256='ef14885b5e334b6ec44a93bfd7225c634247dc946416af3087ab055bf05f54cd')

    def url_for_version(self, version):
        return "file://{0}/g{1}.tgz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
        patch_install_files = self.linda_files_to_patch[self.version.string]
        path_to_filter = self.linda_path_to_filter[self.version.string]
        for filename in patch_install_files:
            if os.path.isfile(filename):
                filter_file(path_to_filter, prefix.bin, join_path(prefix.bin,
                            filename), string='True', backup=False)
                filter_file('/usr/bin/linda', prefix.bin, join_path(prefix.bin,
                            filename), string='True', backup=False)

    def setup_run_environment(self, env):
        ver = self.version.string.split('-')[0]
        env.set('g' + ver + 'root', self.prefix)
        env.set('GAUSSIANHOME', self.prefix)
        env.set('GAUSS_EXEDIR', self.prefix.bin)
        env.set('G' + ver + '_BASIS', self.prefix.bin.basis)
        env.set('GAUSS_LEXEDIR', join_path(self.prefix.bin, 'linda-exe'))
        env.set('GAUSS_ARCHDIR', self.prefix.bin.arch)
        env.set('GAUSS_BSDDIR', self.prefix.bin.bsd)
        env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix.bin,
                         self.linda_directory[self.version.string],
                         'opteron-linux', 'lib'))
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.bin)
