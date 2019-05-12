# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


class Ispc(Package):
    """ispc is a compiler for a variant of the C programming language, with
    extensions for single program, multiple data programming mainly aimed at CPU
    SIMD platforms."""

    homepage = "https://github.com/ispc/ispc/"
    url      = "https://sourceforge.net/projects/ispcmirror/files/v1.11.0/ispc-v1.11.0-linux.tar.gz"

    version('1.11.0', sha256='dae7d1abf950dea722fe3c535e4fa43a29c0b67b14d66e566ab2fa760ee82f38')
    version('1.10.0', sha256='453211ade91c33826f4facb1336114831adbd35196d016e09d589a6ad8699aa3')

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/ispcmirror/files/v{0}/ispc-v{0}-{1}.tar.gz"

        system = platform.system()
        if system == 'Darwin':
            checksums = {
                Version('1.11.0'): '5205e0fca11361f8527d3489ee1503fd79ab8511db6399830c052ccf210cc3b7',
                Version('1.10.0'): '2b2e2499549ce09a6597b6b645e387953de84544ecb44307e7ee960c9b742a89'
            }
            self.versions[version] = {'checksum': checksums[version]}
            if self.spec.satisfies('@1.11.0:'):
                return url.format(version, 'MacOs')
            else:
                return url.format(version, 'osx')
        else:  # linux
            return url.format(version, 'linux')

    def install(self, spec, prefix):
        for d in ['bin', 'examples']:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d))
