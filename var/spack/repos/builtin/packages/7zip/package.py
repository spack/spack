# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import platform

from spack import *


class _7zip(Package):
    """7-Zip is a file archiver for Windows"""

    homepage = "https://sourceforge.net/projects/sevenzip"
    url = "https://downloads.sourceforge.net/project/sevenzip/7-Zip/21.07/7z2107-src.tar.xz"

    executables = ['7z']

    version('21.07', sha1='fa288b643575e55531929e7a7759b6884982556d')

    variant('link_type', default='shared',
            description='build shared and/or static libraries',
            values=('static', 'shared'), multi=True)

    phases = ['build', 'install']

    @property
    def _7z_src_dir(self):
        return os.path.join(self.stage.source_dir, 'CPP', '7zip')

    def is_64bit(self):
        return platform.machine().endswith('64')

    def build(self, spec, prefix):
        link_type = '1' if 'static' in spec.variants['link_type'].value else '0'
        nmake_args = ['MY_STATIC_LINK=%s' % link_type, 'NEW_COMPILER=1']
        with working_dir(self._7z_src_dir):
            nmake(*nmake_args)

    def install(self, spec, prefix):
        """7Zip exports no install target so we must hand install"""
        prefix = 'x64' if self.is_64bit() else 'x86'
        path_roots = ['Bundles', 'UI']
        exts = ['*.exe', '*.zip']
        with working_dir(self._7z_src_dir):
            for root in path_roots:
                pth = os.path.join(root, '*', prefix)
                for ext in exts:
                    glob_str = os.path.join(pth, ext)
                    files = glob.glob(glob_str)
                    [copy(x) for x in files]

